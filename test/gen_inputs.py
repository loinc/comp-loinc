"""Generates subsected inputs to allow for fast testable builds.


Takes input release files (LOINC, SNOMED, etc) and subsects them. Then, a build will be run and outputs of that will be
test inputs.

TODO: add cli
 - cache option
 - should be able to subesct or gen test outputs independently
"""
from pathlib import Path
from typing import Dict, List, Union

try:
    # noinspection PyUnresolvedReferences pycharm_confused_by_test_root
    from test.config import PROJECT_DIR, TEST_IN_DIR_SUBSET as OUTDIR, BUILD_CONFIG_PATH, SUBSET_BUILD_GEN_INPUTS
    from loinclib import Configuration
except ModuleNotFoundError:
    from config import PROJECT_DIR, TEST_IN_DIR_SUBSET as OUTDIR, BUILD_CONFIG_PATH, SUBSET_BUILD_GEN_INPUTS
    from loinclib import Configuration


# TODO: make dirs if don't exist
#  - all subset dirs. do that here at top of file, or maybe in each func


def run_subsect_build():
    """For outputs to be stored after running build on subsected release files"""
    # TODO: TEST_BUILD_CONFIG_PATH instead of BUILD_CONFIG_PATH
    # TODO: override config.logging.loggers.''.level to 'DEBUG'
    config_wrapper = Configuration(SUBSET_BUILD_GEN_INPUTS, BUILD_CONFIG_PATH)
    # TODO: How to pass alternative config path?
    #  - do i need to?
    #  - is that a CLI option?
    #    - if not, a. add one, b. temporarily replace config at root. | 'a' seems much better
    print()


def gen_subsect_config():
    """Generate a comploinc_config.yaml, but for subsected releases"""
    # TODO: create file: in subset_build/ prolly
    #  1. copy from comploinc_config.yaml
    #  2. recurse vals where startswith loinc_release/, loinc_snomed_release/, loinc_trees/, or snomed_release/
    #    - change val if to put in new dir
    #    - write yaml to new location
    # TODO: input dirs: configure them from subset_build/input/
    # TODO: output dir
    print()


def _get_input_paths(
    home_path: Union[str, Path] = SUBSET_BUILD_GEN_INPUTS, config_path: Union[str, Path] = BUILD_CONFIG_PATH
) -> Dict[str, Union[Path, List[Path]]]:
    """Get input paths from config"""
    config_wrapper = Configuration(home_path, config_path)
    config = config_wrapper.config
    # todo: Maybe re-use existing build logic for resolving these paths
    loinc_snomed_release_files: List[Path] = [PROJECT_DIR / x
        for x in config['loinc_snomed']['release'][config['loinc_snomed']['release']['default']]['files'].values()]
    snomed_release_files: List[Path] = [PROJECT_DIR / x
        for x in config['snomed']['release'][config['snomed']['release']['default']]['files'].values()]
    input_paths: Dict[str, Union[Path, List[Path]]] = {
        'loinc_release': PROJECT_DIR / config['loinc']['release'][config['loinc']['release']['default']]['path'],
        'loinc_snomed_release': loinc_snomed_release_files,
        'loinc_trees': PROJECT_DIR / config['loinc_tree']['release'][config['loinc_tree']['release']['default']]['tree_path'],
        'snomed_release': snomed_release_files,
    }
    # TODO: Create empty dirs for each of the release dirs, into
    #  - i think they will be stored as attributes in `vonfig`
    return input_paths

def subsect_releases(use_cache=False):
    """For subsected release files to be stored"""
    input_paths: Dict[str, Union[Path, List[Path]]] = _get_input_paths()
    # TODO: Recurse dirs, find files, and subsect them
    #  a. preconfigured paths to all inputs  <-- easier at first
    #    - but then I have to go through and figure out all the files to use. they might be referenced in builder or
    #    similar classs
    #  b. just do everything
    #    - disadvantage is that not all files are input files.
    #  - how did shahim handle tab vs comma or other delim? Are they all tab?
    print()


def gen_test_inputs():
    """Generate test inputs"""
    subsect_releases()
    gen_subsect_config()
    run_subsect_build()


if __name__ == "__main__":
    gen_test_inputs()
