from unittest import TestCase

from autosettings import PathFinder

from unittest.mock import patch

import os
import sys

class TestPathFinderConstructor(TestCase):
    def test_default_parameters(self):
        result = PathFinder()
        self.assertEqual(result.config_directory_name, "python_autosettings")
        self.assertEqual(result.default_folder_method, "user_config_directory")
        self.assertEqual(len(result.method_resolution_order), 3)
        mro = result.method_resolution_order
        self.assertEqual(mro[0], "dunder_main_directory")
        self.assertEqual(mro[1], "user_config_directory")
        self.assertEqual(mro[2], "system_config_directory")

    def test_non_existing_default_folder_method(self):
        with self.assertRaises(AttributeError) as err:
            PathFinder(default_folder_method="moose")
        expected_message = "'PathFinder' object has not attribute 'moose'"
        self.assertEqual(str(err.exception), expected_message)

    def test_non_callable_default_folder_method(self):
        with self.assertRaises(TypeError) as err:
            PathFinder(default_folder_method="__dict__")
        expected_message = "'__dict__' is not a callable member of the 'PathFinder' class"
        self.assertEqual(str(err.exception), expected_message)

    def test_non_existing_method_resolution_order_item(self):
        with self.assertRaises(AttributeError) as err:
            PathFinder(method_resolution_order=("moose", ))
        expected_message = "'PathFinder' object has not attribute 'moose'"
        self.assertEqual(str(err.exception), expected_message)

    def test_non_callable_method_resolution_order_item(self):
        with self.assertRaises(TypeError) as err:
            PathFinder(method_resolution_order=("__dict__", ))
        expected_message = "'__dict__' is not a callable member of the 'PathFinder' class"
        self.assertEqual(str(err.exception), expected_message)

class TestPathFinderFolderMethods(TestCase):
    def test_get_user_config_directory(self):
        finder = PathFinder()
        result = finder.user_config_directory()
        expected = os.path.join(
            os.path.abspath(os.path.expanduser('~')),
            '.config/python_autosettings')
        self.assertEqual(result, expected)

    def test_get_system_config_directory(self):
        finder = PathFinder()
        result = finder.system_config_directory()
        expected = '/etc/python_autosettings'
        self.assertEqual(result, expected)

    def test_get_dunder_main_directory(self):
        finder = PathFinder()
        result = finder.dunder_main_directory()
        expected = os.path.abspath(os.path.dirname(sys.argv[0]))
        self.assertEqual(result, expected)


class TestPathFinderAbsoluteConfigFilepath(TestCase):
    @patch('os.path.isfile')
    def test_case_when_no_files_exist(self, mock_isfile):
        mock_isfile.return_value = False
        finder = PathFinder(default_folder_method='system_config_directory')
        result = finder.absolute_config_filepath('test.ini')
        expected = '/etc/python_autosettings/test.ini'
        self.assertEquals(result, expected)

    @patch('os.path.isfile')
    def test_case_when_a_file_exists(self, mock_isfile):
        finder = PathFinder()

        def side_effect(filepath):
            helper_method = finder._get_full_filepath
            system_path = helper_method('system_config_directory', 'test.ini')
            print(filepath, system_path)
            return filepath == system_path
        mock_isfile.side_effect = side_effect
        result = finder.absolute_config_filepath('test.ini')
        expected = '/etc/python_autosettings/test.ini'
        self.assertEquals(result, expected)
