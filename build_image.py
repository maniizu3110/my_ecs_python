import os
import time
import shutil
from git import Repo, Actor, GitCommandError
from setup import config
from requests.auth import HTTPBasicAuth
import contextlib
from github import Github
from setup import env
import argparse

# DEFAULT_BRANCH = "develop"
DEFAULT_BRANCH = "main"
WORK_BRANCH_NAME = "feature/add-file-from-backstage"
WORKFLOW_FILE = ".github/workflows/build_template.yaml"


def get_aws_resource_info_for_worklfow(branch_name) -> dict:
    return {
        "$AWS_REGION": env.aws_region,
        "$ECR_REPOSITORY": env.default_service_name,
        "$ENV_S3_BUCKET": env.default_service_name,
        "$DOCKERFILE_NAME": env.dockerfile_name,
        "$BUILD_PATH": env.build_path,
        "$BRANCH_NAME":  branch_name,
    }


def replaceFileContent(workflow_file, branch_name):
    replace_dict = get_aws_resource_info_for_worklfow(branch_name)
    with open(workflow_file, "r") as f:
        content = f.read()
    for key, value in replace_dict.items():
        print(f"Replacing {key} with {value} in {workflow_file}")
        content = content.replace(key, value)
    with open(workflow_file, "w") as f:
        f.write(content)


@contextlib.contextmanager
def temporary_directory(dir_name):
    os.makedirs(dir_name, exist_ok=True)
    try:
        yield dir_name
    finally:
        shutil.rmtree(dir_name)


def get_owner_and_repo(github_repository_url):
    owner_and_repo = github_repository_url.split("github.com/")[1]
    if owner_and_repo.endswith(".git"):
        owner_and_repo = owner_and_repo[:-4]
    return owner_and_repo


def clone(github_repository_url, repo_dir, github_token):
    auth_repo_url = github_repository_url.replace(
        "https://", f"https://{github_token}@") + ".git"
    repo = Repo.clone_from(auth_repo_url, repo_dir)
    print(f"Cloned repository: {github_repository_url}")
    return repo


def add_file(workflow_file, repo_dir, branch_name):
    workflow_file_path = os.path.join(repo_dir, workflow_file)
    os.makedirs(os.path.dirname(workflow_file_path), exist_ok=True)
    shutil.copy(workflow_file, workflow_file_path)
    replaceFileContent(workflow_file_path, branch_name)
    print(f"Copied workflow file to {workflow_file_path}")


def commit(repo, workflow_file, new_branch_name):
    repo.index.add([workflow_file])
    author = Actor("maniizu3110", "maniizu3110@gmail.com")
    commit_message = f"Add {workflow_file}"
    repo.index.commit(commit_message, author=author)
    print(f"Committed {workflow_file} to the {new_branch_name} branch")


def push(repo, new_branch_name):
    origin = repo.remote("origin")
    try:
        origin.push(new_branch_name)
        print(f"Pushed {new_branch_name} branch to the remote repository")
    except GitCommandError as error:
        print(f"Error pushing the new branch: {error}")


def create_pr(repo, github_token, new_branch_name, base_branch_name, github_repository_url, workflow_file):
    # Create a pull request using the PyGithub library
    github = Github(github_token)
    repo = github.get_repo(get_owner_and_repo(github_repository_url))
    base_branch_name = DEFAULT_BRANCH

    try:
        pr = repo.create_pull(
            title=f"[Backstage] Add template file:{workflow_file}",
            body=f"Adding the {workflow_file} file to the {base_branch_name} branch.",
            head=new_branch_name,
            base=base_branch_name,
        )
        print(f"Created pull request: {pr.html_url}")
    except Exception as error:
        print(f"Error creating pull request: {error}")


def checkout(repo, new_branch_name):
    repo.create_head(new_branch_name)
    repo.git.checkout(new_branch_name)
    print(f"Checked out {new_branch_name} branch")


def set_workflow_secret(github_token):
    secrets = {
        "AWS_ACCESS_KEY_ID": env.aws_access_key_id,
        "AWS_SECRET_ACCESS_KEY": env.aws_secret_access_key,
    }
    github = Github(github_token)
    repo = github.get_repo(get_owner_and_repo(env.github_repository_url))
    for key, value in secrets.items():
        ok = repo.create_secret(key, value)
        if ok:
            print(f"Created secret {key}")
        else:
            print(f"Error creating secret {key}")


def wait_for_github_actions_to_finish(branch_name):
    github = Github(os.environ["PERSONAL_ACCESS_TOKEN"])
    repo = github.get_repo(get_owner_and_repo(env.github_repository_url))
    while True:
        time.sleep(10)
        actions = repo.get_workflow_runs(branch=branch_name)
        print("Waiting for actions to finish...")
        for action in actions:
            print(
                f"Action: {action.id}, Status: {action.status}, Conclusion: {action.conclusion}")
        if actions.totalCount == 0:
            print("No actions found")
            break
        if all([action.status == "completed" for action in actions]):
            # TODO:指定のアクションが成功したかどうかを確認する処理の追加
            print("Actions completed!")
            break


def add_workflow_to_github_repository(workflow_file, github_repository_url):
    github_token = os.environ["PERSONAL_ACCESS_TOKEN"]
    new_branch_name = WORK_BRANCH_NAME+"-"+str(int(time.time()))

    with temporary_directory("github_tmp") as repo_dir:
        # Clone the repository
        repo = clone(github_repository_url, repo_dir, github_token)

        add_file(workflow_file, repo_dir, new_branch_name)

        checkout(repo, new_branch_name)

        commit(repo, workflow_file, new_branch_name)
        set_workflow_secret(github_token)

        push(repo, new_branch_name)

        create_pr(repo, github_token, new_branch_name,
                  DEFAULT_BRANCH, github_repository_url, workflow_file)

        wait_for_github_actions_to_finish(new_branch_name)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add a workflow file to a GitHub repository.")
    parser.add_argument(
        "--workflow-file", help="Path to the workflow file.", default=WORKFLOW_FILE)
    parser.add_argument("--github-repository-url",
                        help="URL of the GitHub repository.",
                        default=env.github_repository_url)
    args = parser.parse_args()
    add_workflow_to_github_repository(
        workflow_file=args.workflow_file, github_repository_url=args.github_repository_url)
