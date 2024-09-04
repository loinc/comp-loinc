import logging
import os.path
import re
import time
import typing as t
from pathlib import Path

import typer

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'loinc_trees'

COMPLOINC_OUT_DIR_NAME = 'comploinc_out'


class CompLoincCli:

    def __init__(self):
        self.work_dir: t.Optional[Path] = None
        self.loinc_release_path: t.Optional[Path] = None
        self.loinc_trees_path: t.Optional[Path] = None
        self.loinc_version = None
        self.output_dir = None

        self.cli = typer.Typer(chain=True)
        self.cli.callback(invoke_without_command=True)(self.callback)
        self.cli.command()(self.parts_list)

    def callback(self, /, *,
                 work_dir: t.Annotated[t.Optional[Path], typer.Option(help='CompLOINC work directory.')] = Path.cwd(),
                 loinc_release: t.Annotated[t.Optional[Path], typer.Option(
                     help=f'Path to a directory containing an unpacked LOINC release. Defaults to: ./{LOINC_RELEASE_DIR_NAME}')] = None,
                 loinc_trees: t.Annotated[t.Optional[Path], typer.Option(
                     help=f'A directory name to load tree files from. Defaults to {LOINC_TREES_DIR_NAME}')] = None,

                 loinc_version: t.Annotated[t.Optional[str], typer.Option(
                     help='The LOINC release version. It uses the directory name of the the loinc_release option by if it appears to be a release number.')] = None,

                 out_dir: t.Annotated[t.Optional[Path], typer.Option(help='The CompLOINC output directory.')] = None,
                 log_level: t.Annotated[str, typer.Option(help='Logging level. Defaults to WARN.')] = 'WARN',
                 owl_output: t.Annotated[bool, typer.Option()] = True,
                 rdf_output: t.Annotated[bool, typer.Option()] = True
                 ):

        if not work_dir.exists():
            raise ValueError(f'Work directory: {work_dir} does not exist.')
        self.work_dir = work_dir.absolute()
        self.loinc_release_path = CompLoincCli._find_loinc_release_path(loinc_release, self.work_dir)
        self.loinc_trees_path = CompLoincCli._find_trees_path(loinc_trees, self.work_dir)

        # todo: implement debug
        from pprint import pprint
        pprint(vars(self))

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
        print(self.loinc_trees_path)
        print(self.loinc_version)
        print(self.output_dir)

    def parts_list(self):
        print('parts list')

    @classmethod
    def _find_loinc_release_path(cls, loinc_dir: Path, work_dir: Path) -> Path:
        loinc_release_path = None
        if loinc_dir:
            if not os.path.isabs(loinc_dir):
                loinc_release_path = work_dir / loinc_dir
            else:
                loinc_release_path = loinc_dir
        else:
            loinc_release_path = work_dir / LOINC_RELEASE_DIR_NAME
        loinc_release_path = loinc_release_path.resolve()
        if not (loinc_release_path / 'LoincTable').exists():
            raise ValueError(f'LOINC release path {loinc_release_path}/LoincTable is not found.')
        return loinc_release_path

    @classmethod
    def _find_trees_path(cls, loinc_trees: Path, work_dir: Path) -> Path:
        loinc_trees_path = None
        if loinc_trees:
            if not os.path.isabs(loinc_trees):
                loinc_trees_path = work_dir / loinc_trees
            else:
                loinc_trees_path = loinc_trees
        else:
            loinc_trees_path = work_dir / LOINC_TREES_DIR_NAME
        loinc_trees_path = loinc_trees_path.resolve()
        if not (loinc_trees_path / 'class.csv').exists():
            raise ValueError(f"LOINC tree file {loinc_trees_path / 'class.csv'} does not exist")
        return loinc_trees_path


cli = CompLoincCli()
