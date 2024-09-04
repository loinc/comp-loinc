from __future__ import annotations

import logging.config
import sys
import typing as t
from pathlib import Path
from sys import argv

import typer

from comp_loinc import Runtime
from comp_loinc.loinc_builder_steps import LoincBuilderSteps
from comp_loinc.snomed_builder_steps import SnomedBuilderSteps
from loinclib import Configuration

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'loinc_trees'

COMPLOINC_OUT_DIR_NAME = 'comploinc_out'


class BuilderCli:

  def __init__(self, runtime: Runtime):
    self.runtime = runtime

    self.cli = typer.Typer(chain=True)
    self.cli.callback(invoke_without_command=True)(self.callback)

    self.cli.command('set-module')(self.set_current_module)

  def callback(self):
    pass

  def set_current_module(self,
      name: t.Annotated[str, typer.Option('--name', '-n', help='Set the current module to this name.')]):
    from comp_loinc.module import Module
    if name not in self.runtime.modules:
      self.runtime.modules[name] = Module(name=name, runtime=self.runtime)
    self.runtime.current_module = self.runtime.modules[name]


class CompLoincCli:

  def __init__(self):
    self.work_dir = None
    self.config: t.Optional[Configuration] = None
    self.runtime: t.Optional[Runtime] = None

    self.cli = typer.Typer()
    self.cli.callback(invoke_without_command=True)(self.callback)

    self.builder_cli = BuilderCli(runtime=self.runtime)
    self.cli.add_typer(self.builder_cli.cli, name='builder')

    self.loinc_builders = LoincBuilderSteps(configuration=self.config)
    self.loinc_builders.setup_builder(self.builder_cli)

    self.snomed_builders = SnomedBuilderSteps(configuration=self.config)
    self.snomed_builders.setup_cli_builder_steps_all(self.builder_cli)

  def callback(self, *,
      work_dir: t.Annotated[
        t.Optional[Path], typer.Option(help='CompLOINC work directory, defaults to current work directory.',
                                       default_factory=Path.cwd)],
      config_file: t.Annotated[
        t.Optional[Path], typer.Option(help='Configuration file name. Defaults to "comploinc_config.yaml"')] = Path(
          'comploinc_config.yaml'),

      output_dir: t.Annotated[t.Optional[Path], typer.Option('--out-dir', '-o',
                                                             help='The output folder name. Defaults to "output".')] = 'output',

      fast_run: t.Annotated[
        bool, typer.Option(help='Turns on a fast run feature which is useful for development.', hidden=True)] = False,

      # graph_path: t.Annotated[
      #   t.Optional[Path], typer.Option(help='Pickled graph path, relative to current work directory path')] = None,
      #
      # loinc_release: t.Annotated[t.Optional[Path], typer.Option(
      #     help=f'Path to a directory containing an unpacked LOINC release. Defaults to: ./{LOINC_RELEASE_DIR_NAME}')] = None,
      #
      # pickled_path: t.Annotated[
      #   t.Optional[Path], typer.Option(help='Path to an already pickled loinclib graph.')] = None,
      #
      # to_pickle_path: t.Annotated[
      #   t.Optional[Path], typer.Option(help='A path to which  the loinclib Graph will be saved to.')] = None,

  ):
    self.work_dir = work_dir.absolute()
    if not self.work_dir.exists():
      raise ValueError(f'Work directory: {self.work_dir} does not exist.')

    self.config = Configuration(home_path=self.work_dir, config_file=config_file.absolute())
    self.config.fast_run = fast_run
    self.config.output = self.work_dir / output_dir

    logging.config.dictConfig(self.config.get_logging_configuration())

    self.loinc_builders.configuration = self.config
    self.snomed_builders.configuration = self.config

    self.runtime = Runtime(configuration=self.config, name='cli')
    self.loinc_builders.runtime = self.runtime
    self.snomed_builders.runtime = self.runtime

    self.builder_cli.runtime = self.runtime


comploinc_cli = CompLoincCli().cli


def comploinc_file_cli():
  cwd = Path.cwd()
  cli_file_path = Path(argv[1])
  if not cli_file_path.is_absolute():
    cli_file_path = cwd / cli_file_path

  args = ['comploinc-file']
  with open(cli_file_path, 'r') as f:
    for line in f:
      line = line.strip()
      if line and not line.startswith('#'):
        args.append(line)

  sys.argv = args
  print(f'running command: {args}')

  comploinc_cli()
