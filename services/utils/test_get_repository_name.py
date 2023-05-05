import unittest
from get_repository_name import change_to_pascal_case


class TestChangeToValidRepositoryName(unittest.TestCase):

    def test_no_change(self):
        self.assertEqual(change_to_pascal_case(
            "ValidRepoName"), "ValidRepoName")

    def test_dash_to_camel_case(self):
        self.assertEqual(change_to_pascal_case(
            "invalid-repo-name"), "invalidRepoName")

    def test_underscore_to_camel_case(self):
        self.assertEqual(change_to_pascal_case(
            "invalid_repo_name"), "invalidRepoName")

    def test_dash_and_underscore_to_camel_case(self):
        self.assertEqual(change_to_pascal_case(
            "invalid-repo_name"), "invalidRepoName")

    def test_only_dash(self):
        self.assertEqual(
            change_to_pascal_case("invalid-"), "invalid")

    def test_only_underscore(self):
        self.assertEqual(
            change_to_pascal_case("invalid_"), "invalid")


if __name__ == "__main__":
    unittest.main()
