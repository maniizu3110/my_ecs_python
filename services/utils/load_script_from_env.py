yaml_space_for_github_actions_step = "          "

def load_pre_build_script(filepath: str) -> str:
    pre_build_script = ""
    reading_pre_build_script = False
    with open(filepath) as file:
        for line in file:
            if line.startswith('PRE_BUILD_SCRIPT='):
                reading_pre_build_script = True
                line = line[len("PRE_BUILD_SCRIPT="):].rstrip()
            elif reading_pre_build_script and line[0].isupper() and "=" in line:
                break  # Stop reading when encountering the next uppercase key with an equal sign

            if reading_pre_build_script:
                pre_build_script += yaml_space_for_github_actions_step + line.rstrip() + '\n'

    return pre_build_script.rstrip()
