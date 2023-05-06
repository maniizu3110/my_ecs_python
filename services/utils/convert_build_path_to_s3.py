import re

def convert_to_s3_object_name(build_path: str) -> str:
    return re.sub(r'\./|/$', '', build_path).replace('/', '-')
