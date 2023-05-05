from urllib.parse import urlparse


def get_repository_name(url: str) -> str:
    parsed_url = urlparse(url)
    repository_name = parsed_url.path.split("/")[-1]
    if repository_name.endswith(".git"):
        repository_name = repository_name[:-4]
    return repository_name


# change to camel case
def change_to_pascal_case(repository_name: str) -> str:
    if repository_name.find("-") != -1 or repository_name.find("_") != -1:
        repository_name = repository_name.replace("-", "_")
        words = repository_name.split("_")
        repository_name = words[0] + \
            "".join(word.capitalize() for word in words[1:])
    return repository_name


# change snake case to camel case
def change_to_camel_case(name: str) -> str:
    if name.find("_") != -1:
        words = name.split("_")
        name = words[0] + \
            "".join(word.capitalize() for word in words[1:])
    return name
