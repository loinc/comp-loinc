import logging
import re
import time
import typing as t
from pathlib import Path

import typer

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'trees'


class CompLoincCli:

    def __init__(self):
        self.loinc_release_path: t.Optional[Path] = None
        self.loinc_release_trees_path: t.Optional[Path] = None
        self.loinc_version = None
        self.output_dir = None

        self.typer = typer.Typer()
        self.typer.callback()(self.callback)
        self.typer.command()(self.parts_list)

    def callback(self, /, *,
                 loinc_dir: t.Annotated[t.Optional[Path], typer.Option(
                     help='Path to a directory containing an unpacked LOINC release. '
                          './loinc_release by default.')] = None,
                 tree_directory_name: t.Annotated[t.Optional[str], typer.Option(
                     help='A directory name to load tree files from. For example, '
                          '"2023-01-01" would look for tree files in loinc_release/trees/2023-01-01')] = None,
                 loinc_version: t.Annotated[t.Optional[str], typer.Option(
                     help='The LOINC release version. It uses the directory name of the LOINC directory by '
                          'default if it appears to be a release number.')] = None,
                 out_dir: t.Annotated[t.Optional[Path], typer.Option(help='The CompLOINC output directory.')] = None,
                 log_level: t.Annotated[str, typer.Option(help='Logging level. Defaults to WARN.')] = 'WARN',
                 owl_output: t.Annotated[bool, typer.Option()] = True,
                 rdf_output: t.Annotated[bool, typer.Option()] = True
                 ):

        if loinc_dir:
            if (loinc_dir / 'LoincTable').exists():
                self.loinc_release_path = loinc_dir
            else:
                raise ValueError(f'LOINC release path {loinc_dir}/LoincTable is not found.')
        else:
            self._find_loinc_release_path()

        if tree_directory_name:
            tree_dir = self.loinc_release_path / 'trees' / tree_directory_name
            if tree_dir.exists():
                if (tree_dir / 'class.csv').exists():
                    self.loinc_release_trees_path = tree_dir
                else:
                    raise ValueError(f"LOINC tree file {tree_dir / 'class.csv'} does not exist")
            else:
                raise ValueError(f'LOINC tree directory {tree_dir} does not exist.')
        else:
            self._find_loinc_release_trees_path()

        if loinc_version is None:
            loinc_version = self.loinc_release_path.name

        if re.match(r'[0-9]\.[0-9]+', loinc_version):
            self.loinc_version = loinc_version
        else:
            raise ValueError(f'LOINC version {loinc_version} does not appear to be a valid version.')

        if out_dir:
            self.output_dir = out_dir
        else:
            self.output_dir = Path.cwd() / 'comp_loinc'

        log_dir = self.output_dir / 'logs'
        log_dir.mkdir(parents=True, exist_ok=True)
        logging.basicConfig(filename=log_dir / f'log_{time.strftime("%Y%m%d-%H%M%S")}.txt',
                            encoding='utf-8',
                            level=logging.getLevelName(log_level.upper())
                            )

        print(self.loinc_release_path)
        print(self.loinc_release_trees_path)
        print(self.loinc_version)
        print(self.output_dir)

    def parts_list(self):
        print('parts list')

    def _find_loinc_release_path(self):
        loinc_base_path = Path.cwd() / LOINC_RELEASE_DIR_NAME

        if (loinc_base_path / 'LoincTable').exists():
            self.loinc_release_path = loinc_base_path
        else:
            for d in reversed(sorted(list(loinc_base_path.glob('*')))):
                if Path.is_dir(d):
                    if (loinc_base_path / d / 'LoincTable').exists():
                        self.loinc_release_path = loinc_base_path / d
                        break

        if self.loinc_release_path is None:
            raise ValueError("Couldn't find LOINC release directory.")

    def _find_loinc_release_trees_path(self):
        loinc_trees_path = self.loinc_release_path / LOINC_TREES_DIR_NAME
        if (loinc_trees_path / 'class.csv').exists():
            self.loinc_release_trees_path = loinc_trees_path
        else:
            for d in reversed(sorted(list(loinc_trees_path.glob('*')))):
                if Path.is_dir(d):
                    if (loinc_trees_path / d / 'class.csv').exists():
                        self.loinc_release_trees_path = loinc_trees_path / d
                        break

        if self.loinc_release_trees_path is None:
            raise ValueError("Couldn't find LOINC trees directory.")


cli = CompLoincCli().typer
