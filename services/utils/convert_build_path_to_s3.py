import re


def convert_path_to_object_name(build_path: str) -> str:
    return re.sub(r'\./|/$', '', build_path).replace('/', '-')
