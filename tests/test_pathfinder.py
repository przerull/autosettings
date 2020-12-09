from unittest import TestCase

from autosettings import PathFinder

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
