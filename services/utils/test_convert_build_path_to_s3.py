import unittest
from .convert_build_path_to_s3 import convert_path_to_object_name


class TestConvertToS3ObjectName(unittest.TestCase):

    def test_convert_go_hey(self):
        self.assertEqual(convert_path_to_object_name('./go/hey'), 'go-hey')

    def test_convert_build_path(self):
        self.assertEqual(convert_path_to_object_name(
            './build/path/'), 'build-path')

    def test_convert_some_other_path(self):
        self.assertEqual(convert_path_to_object_name(
            './some/other.path/'), 'some-other.path')

    def test_convert_empty_string(self):
        self.assertEqual(convert_path_to_object_name('./'), '')

    def test_convert_path_without_dots(self):
        self.assertEqual(convert_path_to_object_name(
            'some/path/without/dots'), 'some-path-without-dots')


if __name__ == '__main__':
    unittest.main()
