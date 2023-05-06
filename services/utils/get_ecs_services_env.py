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


