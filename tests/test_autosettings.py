from unittest import TestCase

import autosettings


import os
import sys
from io import BytesIO

class TestSettingsDefaults(autosettings.Schema):
    integer_field = autosettings.IntegerField(1)
    string_field = autosettings.StringField("default_value")


class TestSettingsNoDefaults(autosettings.Schema):
    integer_field = autosettings.IntegerField()
    string_field = autosettings.StringField()



class TestMain(TestCase):
    def test_load_empty_file_with_defaults(self):
        fileref = BytesIO()
        settings = TestSettingsDefaults(fileref)
        self.assertEqual(settings.integer_field, 1)
        self.assertEqual(settings.string_field, "default_value")

    def test_load_empty_file_no_defaults(self):
        fileref = BytesIO()
        settings = TestSettingsNoDefaults(fileref)
        self.assertEqual(settings.integer_field, None)
        self.assertEqual(settings.string_field, None)

    def test_setting_invalid_integer(self):
        fileref = BytesIO()
        settings = TestSettingsNoDefaults(fileref)
        with self.assertRaises(TypeError):
            settings.integer_field = "moose"

    def test_setting_invalid_string(self):
        fileref = BytesIO()
        settings = TestSettingsNoDefaults(fileref)
        with self.assertRaises(TypeError):
            settings.string_field = 12

    def test_singleton_behavior(self):
        file1 = BytesIO()
        file2 = BytesIO()
        settings1 = TestSettingsDefaults(file1)
        settings2 = TestSettingsDefaults(file2)
        self.assertEqual(settings1.integer_field, 1)
        self.assertEqual(settings2.integer_field, 1)
        settings1.integer_field = 3
        self.assertEqual(settings1.integer_field, 3)
        self.assertEqual(settings2.integer_field, 3)

    def test_to_dictionary(self):
        fileref = BytesIO()
        settings = TestSettingsNoDefaults(fileref)
        settings.integer_field = 5
        result = settings.to_dictionary()
        expected_result = dict(
            integer_field = 5,
            string_field = None)
        self.assertEqual(result, expected_result)
