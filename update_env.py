import boto3
import json
from services.utils.convert_build_path_to_s3 import convert_to_s3_object_name
from services.utils.get_repository_name import get_repository_name
from setup import config, env


def get_rds_info(service_name) -> dict:
    secretsmanager_client = boto3.client('secretsmanager')

    secret_list_response = secretsmanager_client.list_secrets()
    for secret in secret_list_response['SecretList']:
        if service_name in secret['Name']:
            secret_response = secretsmanager_client.get_secret_value(
                SecretId=secret['ARN'])
            secret_value = json.loads(secret_response['SecretString'])

            replace_dict = {
                "$DB_HOST": secret_value['host'],
                "$DB_USER": secret_value['username'],
                "$DB_PASSWORD": secret_value['password'],
                "$DB_NAME": secret_value['dbname'],
            }
            return replace_dict


def downloadEnvOfApp(bucket, env_file_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).download_file(env_file_name, 'tmp.env')


def uploadEnvOfApp(bucket, env_file_name):
    s3 = boto3.resource('s3')
    s3.Bucket(bucket).upload_file('tmp.env', env_file_name)


def replaceEnvContentWithDict(replace_dict):
    # Read the content of the env file
    with open('tmp.env', 'r') as f:
        env_content = f.read()

    # Replace the old value with the new value
    for key, value in replace_dict.items():
        env_content = env_content.replace(key, value)

    # Write the updated content back to the env file
    with open('tmp.env', 'w') as f:
        f.write(env_content)


def replaceEnvInS3(replace_dict: dict, service_name: str):
    env_file_name = f"{get_repository_name(env.github_repository_url)}-{convert_to_s3_object_name(env.build_path)}.env"
    downloadEnvOfApp(service_name, env_file_name)
    replaceEnvContentWithDict(replace_dict)
    uploadEnvOfApp(service_name, env_file_name)


def main():
    # TODO:service_nameの違いはwrapperで吸収する
    replace_dict = get_rds_info(config.pascal_service_name)
    replaceEnvInS3(replace_dict, config.default_service_name)


if __name__ == "__main__":
    main()
