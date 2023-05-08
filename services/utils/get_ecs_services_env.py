import boto3


def list_env_files(bucket_name):
    s3_client = boto3.client('s3')

    # Check if the specified bucket exists
    try:
        s3_client.list_objects(Bucket=bucket_name)
    except s3_client.exceptions.NoSuchBucket:
        print(f"S3 bucket not found: {bucket_name}")
        return []

    # List objects in the specified bucket
    objects = s3_client.list_objects(Bucket=bucket_name)

    # Filter .env files from the object keys (file names)
    env_files = [obj['Key']
                 for obj in objects['Contents'] if obj['Key'].endswith('.env')]

    return env_files


def get_file_content(bucket_name, object_name):
    # クライアントを作成
    s3_client = boto3.client('s3')

    # 指定されたバケット内のオブジェクトをリストアップ
    objects = s3_client.list_objects(Bucket=bucket_name)

    # オブジェクトのキー（ファイル名）から.envファイルをフィルタリング
    env_files = [obj['Key']
                 for obj in objects['Contents'] if obj['Key'].endswith('.env')]

    # 指定されたファイル名の.envファイルが存在するか確認
    if object_name not in env_files:
        print(f"File '{object_name}' not found in bucket '{bucket_name}'.")
        return

    # 指定されたファイル名の.envファイルの内容を取得
    content = s3_client.get_object(
        Bucket=bucket_name,
        Key=object_name
    )['Body'].read().decode('utf-8')

    return content


def list_env_file_names(bucket_name):
    env_files = list_env_files(bucket_name)
    env_file_names = [env_file.replace('.env', '') for env_file in env_files]
    return env_file_names


def list_env_file_names_with_prefix(bucket_name, prefix):
    env_file_names = list_env_file_names(bucket_name)
    env_file_names_with_prefix = [
        f"{prefix}-{env_file_name}" for env_file_name in env_file_names]
    return env_file_names_with_prefix
