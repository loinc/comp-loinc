"""Config for tests."""
import os
from pathlib import Path


TEST_DIR = Path(os.path.dirname(__file__))
PROJECT_DIR = TEST_DIR.parent
# TEST_IN_DIR = TEST_DIR / 'input'
TEST_IN_DIR = PROJECT_DIR / 'output' / 'build-default' / 'fast-run'
TEST_OUT_DIR = TEST_DIR / 'output'
TEST_SPARQL_QEURY_DIR = TEST_DIR / 'queries'
ROBOT_JAR_PATH = PROJECT_DIR / 'robot.jar'
