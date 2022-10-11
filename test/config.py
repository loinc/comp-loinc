"""Config for tests."""
import os
from pathlib import Path


TEST_PACKAGES = ['comp_loinc']
TEST_DIR = os.path.dirname(__file__)
PROJECT_DIR = Path(TEST_DIR).parent
TEST_STATIC_DIR = os.path.join(TEST_DIR, 'static')
