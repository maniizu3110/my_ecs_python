import boto3


def list_env_files(bucket_name):
    # クライアントを作成
    s3_client = boto3.client('s3')

    # 指定されたバケット内のオブジェクトをリストアップ
    objects = s3_client.list_objects(Bucket=bucket_name)

    # オブジェクトのキー（ファイル名）から.envファイルをフィルタリング
    env_files = [obj['Key']
                 for obj in objects['Contents'] if obj['Key'].endswith('.env')]

    return env_files


def list_env_file_names(bucket_name):
    env_files = list_env_files(bucket_name)
    env_file_names = [env_file.replace('.env', '') for env_file in env_files]
    return env_file_names


def list_env_file_names_with_prefix(bucket_name, prefix):
    env_file_names = list_env_file_names(bucket_name)
    env_file_names_with_prefix = [
        prefix + env_file_name for env_file_name in env_file_names]
    return env_file_names_with_prefix
