"""Test utils"""
import os
import subprocess
import sys
from pathlib import Path
from typing import Union

import pandas as pd

try:
    from test.config import ROBOT_JAR_PATH, TEST_IN_DIR, TEST_OUT_DIR, TEST_SPARQL_QEURY_DIR
except ModuleNotFoundError:
    from config import ROBOT_JAR_PATH, TEST_IN_DIR, TEST_OUT_DIR, TEST_SPARQL_QEURY_DIR

robot_cmd_options = ['robot', f'java -jar {ROBOT_JAR_PATH}']


def _get_paths(onto_filename: str, sparql_filename: str) -> tuple[str, str, str]:
    """Derive paths for test from filenames of inputs"""
    onto_path: str = TEST_IN_DIR / onto_filename
    sparql_path: str = TEST_SPARQL_QEURY_DIR / sparql_filename
    outname: str = os.path.splitext(os.path.basename(onto_path))[0] + '_' + \
        os.path.splitext(os.path.basename(sparql_path))[0]
    outpath: str = TEST_OUT_DIR / (outname + '.csv')
    return onto_path, sparql_path, outpath


def run_sparql_query(
    onto_path: Union[str, Path], sparql_path: Union[str, Path], outpath: Union[str, Path],
    robot_command: Union[str, Path] = robot_cmd_options[0], verbose=False, raise_on_0_results=True
) -> pd.DataFrame:
    """Run a SPARQL query, and return results."""
    # Run query
    command_str = f'{robot_command} query --input {onto_path} --query {sparql_path} {outpath}'
    result = subprocess.run(command_str.split(), capture_output=True, text=True)
    stderr, stdout = result.stderr, result.stdout
    # -vvv: Some robot exceptions don't say 'error' or 'exception', but -vvv (verbose) is a tell.
    if any([x in y.lower() for x in ['error', 'exception', '-vvv'] for y in [stderr, stdout]]):
        raise RuntimeError(stdout + stderr)
    if verbose:
        print(stdout)
        print(stderr, file=sys.stderr)

    # Read results and return
    try:
         return pd.read_csv(outpath)
    except pd.errors.EmptyDataError as err:
        if raise_on_0_results:
            raise err
        return pd.DataFrame()


def sparql_ask(onto_filename: str, sparql_filename: str) -> bool:
    """Given input names, resolve paths and exec ASK query"""
    df: pd.DataFrame = sparql_select(onto_filename, sparql_filename)
    return list(df.columns)[0].lower() != 'false'


def sparql_select(onto_filename: str, sparql_filename: str) -> pd.DataFrame:
    """Given input names, resolve paths and exec SELECT query"""
    onto_path, sparql_path, outpath = _get_paths(onto_filename, sparql_filename)
    try:
        return run_sparql_query(onto_path, sparql_path, outpath)
    except FileNotFoundError:
        return run_sparql_query(onto_path, sparql_path, outpath, robot_cmd_options[1])
