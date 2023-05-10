from aws_cdk import (
    aws_rds as rds,
)


def get_rds_parameters(king: str) -> dict:
    params = {}
    if king == "mysql":
        params = {
            'character_set_client': 'utf8mb4',
            'character_set_connection': 'utf8mb4',
            'character_set_database': 'utf8mb4',
            'character_set_filesystem': 'utf8mb4',
            'character_set_results': 'utf8mb4',
            'character_set_server': 'utf8mb4',
            'collation_connection': 'utf8mb4_unicode_ci',
            'collation_server': 'utf8mb4_unicode_ci',
        }
    elif king == "postgres":
        params = {
            'client_encoding': 'utf8',
            'standard_conforming_strings': 'off',
            'timezone': 'Asia/Tokyo',
        }
    return params


def get_rds_engine(database_kind: str):
    if database_kind == "mysql":
        return rds.DatabaseInstanceEngine.mysql(
            version=rds.MysqlEngineVersion.VER_5_7_33)

    elif database_kind == "postgres":
        return rds.DatabaseInstanceEngine.postgres(
            version=rds.PostgresEngineVersion.VER_13_3
        )
