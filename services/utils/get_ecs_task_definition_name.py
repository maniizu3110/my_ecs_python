import boto3


def get_task_definition_names(cluster_name, service_name):
    # クライアントを作成
    ecs_client = boto3.client("ecs")

    # クラスター内のサービスをリストアップ
    services = ecs_client.list_services(cluster=cluster_name)["serviceArns"]

    # サービスARNをサービス名に変換
    service_names = [s.split("/")[-1] for s in services]

    # 指定されたサービス名が存在するか確認
    if service_name not in service_names:
        print(
            f"Service '{service_name}' not found in cluster '{cluster_name}'.")
        return

    # サービスの詳細情報を取得
    service = ecs_client.describe_services(cluster=cluster_name, services=[
                                           service_name])['services'][0]

    # タスク定義ARNを取得
    task_definition_arn = service['taskDefinition']

    # タスク定義ARNをタスク定義名に変換
    task_definition_name = task_definition_arn.split("/")[-1]

    # リビジョン番号を削除
    task_definition_name = task_definition_name.split(":")[0]    

    return task_definition_name
