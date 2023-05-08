import re


def convert_path_to_object_name(build_path: str) -> str:
    name = re.sub(r'\./|/$', '', build_path).replace('/', '-')
    return f"-{name}" if name else ''
