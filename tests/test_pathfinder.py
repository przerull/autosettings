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
