import os
import argparse
from github import Github
from set_workflow import WORK_BRANCH_NAME
from setup import env


def delete_pull_request_with_branch(github_token, github_repository_url, branch_name):
    github = Github(github_token)
    repo = github.get_repo(get_owner_and_repo(github_repository_url))

    # Search for the pull requests
    pull_requests = repo.get_pulls(state='open')
    target_pull_requests = []

    for pr in pull_requests:
        if branch_name in pr.head.ref:
            target_pull_requests.append(pr)

    # If pull requests with the specified branch name are found, close them
    if target_pull_requests:
        for target_pr in target_pull_requests:
            target_pr.edit(state='closed')
            print(f"Closed pull request: {target_pr.html_url}")
    else:
        print("No pull request found with the specified branch name")


def get_owner_and_repo(github_repository_url):
    owner_and_repo = github_repository_url.split("github.com/")[1]
    if owner_and_repo.endswith(".git"):
        owner_and_repo = owner_and_repo[:-4]
    return owner_and_repo


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Delete a pull request associated with a specific branch in a GitHub repository.")
    parser.add_argument("--branch-name", help="Name of the branch associated with the pull request.",
                        default=WORK_BRANCH_NAME)
    parser.add_argument("--github-repository-url",
                        help="URL of the GitHub repository.",
                        default=env.github_repository_url)

    args = parser.parse_args()
    github_token = os.environ["PERSONAL_ACCESS_TOKEN"]
    delete_pull_request_with_branch(
        github_token, args.github_repository_url, args.branch_name)
