import unittest
from io import StringIO
from unittest.mock import patch

from .load_script_from_env import load_pre_build_script


class TestLoadPreBuildScript(unittest.TestCase):

    def test_load_pre_build_script(self):
        env_file_content = (
            "HEALTH_CHECK_PATH=/health\n"
            "HEALTH_CHECK_CODES=200-499\n"
            "HEALTH_CHECK_PORT=80\n"
            "HEALTH_CHECK_INTERVAL=30\n"
            "HEALTH_CHECK_TIMEOUT=5\n"
            "HEALTHY_THRESHOLD_COUNT=2\n"
            "UNHEALTHY_THRESHOLD_COUNT=2\n"
            "PRE_BUILD_SCRIPT=#!/bin/bash\n"
            "chmod +x ./scripts/pre_build.sh\n"
            "./scripts/pre_build.sh\n"
        )

        expected_pre_build_script = (
            "#!/bin/bash\n"
            "chmod +x ./scripts/pre_build.sh\n"
            "./scripts/pre_build.sh"
        )

        with patch("builtins.open", return_value=StringIO(env_file_content)):
            pre_build_script = load_pre_build_script(".env")

        self.assertEqual(pre_build_script, expected_pre_build_script)

    def test_load_pre_build_script_stops_at_next_key(self):
        env_file_content = (
            "HEALTH_CHECK_PATH=/health\n"
            "HEALTH_CHECK_CODES=200-499\n"
            "HEALTH_CHECK_PORT=80\n"
            "HEALTH_CHECK_INTERVAL=30\n"
            "HEALTH_CHECK_TIMEOUT=5\n"
            "HEALTHY_THRESHOLD_COUNT=2\n"
            "UNHEALTHY_THRESHOLD_COUNT=2\n"
            "PRE_BUILD_SCRIPT=#!/bin/bash\n"
            "chmod +x ./scripts/pre_build.sh\n"
            "./scripts/pre_build.sh\n"
            "NEXT_UPPERCASE_KEY=value\n"
            "another_line\n"
        )
        expected_pre_build_script = (
            "#!/bin/bash\n"
            "chmod +x ./scripts/pre_build.sh\n"
            "./scripts/pre_build.sh"
        )

        with patch("builtins.open", return_value=StringIO(env_file_content)):
            pre_build_script = load_pre_build_script(".env")

        self.assertEqual(pre_build_script, expected_pre_build_script)

    def test_load_pre_build_script_with_empty_string(self):
        env_file_content = (
            "HEALTH_CHECK_PATH=/health\n"
            "HEALTH_CHECK_CODES=200-499\n"
            "HEALTH_CHECK_PORT=80\n"
            "HEALTH_CHECK_INTERVAL=30\n"
            "HEALTH_CHECK_TIMEOUT=5\n"
            "HEALTHY_THRESHOLD_COUNT=2\n"
            "UNHEALTHY_THRESHOLD_COUNT=2\n"
        )
        expected_pre_build_script = ""

        with patch("builtins.open", return_value=StringIO(env_file_content)):
            pre_build_script = load_pre_build_script(".env")

        self.assertEqual(pre_build_script, expected_pre_build_script)


if __name__ == "__main__":
    unittest.main()
