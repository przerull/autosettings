#!/usr/bin/env python


import coverage
import os
import sys
import unittest
import logging

if '-q' in sys.argv:
    logging.disable(logging.CRITICAL)
cov = coverage.Coverage(branch=True, source=['autosettings'])
if '-q' in sys.argv:
    report_file = open(os.devnull, 'w')
else:
    report_file = None
cov.start()
suite = unittest.TestLoader().discover('tests', '*.py', '.')
result = unittest.TextTestRunner().run(suite)
cov.stop()
number_errors = len(result.errors) + len(result.failures)
total = cov.report(show_missing=True, file=report_file)
cov.html_report()

exit_code = 0
if number_errors > 0:
    exit_code = 1
elif total < 100:
    exit_code = 2

sys.exit(exit_code)
