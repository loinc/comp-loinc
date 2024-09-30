"""Tests"""
import unittest

try:
    from test.config import PROJECT_DIR, TEST_STATIC_DIR
except ModuleNotFoundError:
    from config import PROJECT_DIR, TEST_STATIC_DIR


class CompLoincPythonAPITests(unittest.TestCase):
    """CompLOINC tests"""

    def all(self):
        """Wrapper for running all at once."""
        pass


# Debugging / development
DEBUG = False
if DEBUG:
    CompLoincPythonAPITests().all()
