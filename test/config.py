"""Config for tests."""
import os
from pathlib import Path


TEST_DIR = Path(os.path.dirname(__file__))
PROJECT_DIR = TEST_DIR.parent
BUILD_CONFIG_PATH = PROJECT_DIR / 'comploinc_config.yaml'
SUBSET_BUILD_DIR = TEST_DIR / 'input' / 'subset_build'  # Takes input release files (LOINC, SNOMED, etc) and subsects them. Then, a build will be run and outputs of that will be test inputs.
SUBSET_BUILD_GEN_INPUTS = SUBSET_BUILD_DIR / 'input'  # For subsected release files to be stored
TEST_IN_DIR_SUBSET = SUBSET_BUILD_DIR / 'output'  # For outputs to be stored after running build on subsected release files
TEST_IN_DIR_FAST_RUN = PROJECT_DIR / 'output' / 'build-default' / 'fast-run'
TEST_OUT_DIR = TEST_DIR / 'output'
TEST_SPARQL_QEURY_DIR = TEST_DIR / 'queries'
ROBOT_JAR_PATH = PROJECT_DIR / 'robot.jar'
