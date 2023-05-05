import sys
from pathlib import Path
from get_repository_name import get_repository_name
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parent))


class TestGetRepositoryName(unittest.TestCase):

    def test_get_repository_name_https(self):
        url = "https://github.com/user/repository"
        expected = "repository"
        result = get_repository_name(url)
        self.assertEqual(result, expected)

    def test_get_repository_name_http(self):
        url = "http://github.com/user/repository"
        expected = "repository"
        result = get_repository_name(url)
        self.assertEqual(result, expected)

    def test_get_repository_name_with_dot_git(self):
        url = "https://github.com/user/repository.git"
        expected = "repository"
        result = get_repository_name(url)
        self.assertEqual(result, expected)

    def test_get_repository_name_with_subdirectory(self):
        url = "https://github.com/user/repository/tree/main/subdirectory"
        expected = "subdirectory"
        result = get_repository_name(url)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()
