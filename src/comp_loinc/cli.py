from __future__ import annotations

import logging.config
import typing as t
from pathlib import Path

import typer

from comp_loinc import Runtime
from comp_loinc.groups.groups_builders import GroupsBuilderSteps
from comp_loinc.loinc_builder_steps import LoincBuilderSteps
from comp_loinc.snomed_builder_steps import SnomedBuilderSteps
from loinclib import Configuration

LOINC_RELEASE_DIR_NAME = 'loinc_release'
LOINC_TREES_DIR_NAME = 'loinc_trees'

COMPLOINC_OUT_DIR_NAME = 'comploinc_out'

logger = logging.getLogger('cl-cli')

class BuilderCli:

  def __init__(self, runtime: Runtime):
    self.runtime = runtime

    self.cli = typer.Typer(chain=True)
    self.cli.callback(invoke_without_command=True)(self.callback)

    self.cli.command('set-module')(self.set_current_module)
    self.cli.command('rm-module')(self.remove_module)

  def callback(self):
    pass

  def set_current_module(self,
      name: t.Annotated[str, typer.Option('--name', '-n', help='Set the current module to this name.')]):
    from comp_loinc.module import Module
    if name not in self.runtime.modules:
      self.runtime.modules[name] = Module(name=name, runtime=self.runtime)
    self.runtime.current_module = self.runtime.modules[name]

  def remove_module(self,
      module_name: t.Annotated[str, typer.Option('--name', '-n', help='Removes the named module from the runtime.')]
  ):
    del self.runtime.modules[module_name]
    if self.runtime.current_module.name == module_name:
      self.runtime.current_module = None

class CompLoincCli:

  def __init__(self):
    self.work_dir = None
    self.config: t.Optional[Configuration] = None
    self.runtime: t.Optional[Runtime] = None

    self.cli = typer.Typer()
    self.cli.callback(invoke_without_command=True)(self.callback)

    self.cli.command('build',
                     help='Performs a build from a build file as opposed to the "builder" command which takes build steps.')(
        self.build)

    self.builder_cli = BuilderCli(runtime=self.runtime)
    self.cli.add_typer(self.builder_cli.cli, name='builder')

    self.loinc_builders = LoincBuilderSteps(configuration=self.config)
    self.loinc_builders.setup_builder(self.builder_cli)

    self.snomed_builders = SnomedBuilderSteps(configuration=self.config)
    self.snomed_builders.setup_cli_builder_steps_all(self.builder_cli)

    self.groups_builders = GroupsBuilderSteps(config=self.config)
    self.groups_builders.setup_builder(self.builder_cli)


  def callback(self, *, work_dir: t.Annotated[
    t.Optional[Path], typer.Option(help='CompLOINC work directory, defaults to current work directory.',
                                   default_factory=Path.cwd)], config_file: t.Annotated[
    t.Optional[Path], typer.Option(help='Configuration file name. Defaults to "comploinc_config.yaml"')] = Path(
      'comploinc_config.yaml'),

      output_dir: t.Annotated[t.Optional[Path], typer.Option('--out-dir', '-o',
                                                             help='The output folder name. Defaults to "output".')] = 'output',

      fast_run: t.Annotated[
        bool, typer.Option(help='Turns on a fast run feature which is useful for development.', hidden=True)] = False,

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
    self.groups_builders.config = self.config
    self.groups_builders.runtime = self.runtime

  def build(self,
      build_name: t.Annotated[Path, typer.Argument(help='The build name or a path to a build file.')] = 'default'):
    build_file_path: Path
    if build_name.name.endswith('.txt'):
      if build_name.is_absolute():
        build_file_path = build_name
      else:
        build_file_path = self.work_dir / build_name
    else:
      from comp_loinc import builds_path
      build_file_path = builds_path / build_name.with_suffix('.txt')

    args = []

    if self.config.fast_run:
      args.append('--fast-run')

    args = args + ['--out-dir', f'{self.config.output / f"build-{build_name}"}'] + parse_build_file(build_file_path)

    logger.info(f'Running: {args}')
    self.cli(args)

comploinc_cli = CompLoincCli().cli

def parse_build_file(build_file_path: Path):
  args = []
  with open(build_file_path, 'r') as f:
    for line in f:
      line = line.strip()
      if line and not line.startswith('#'):
        args.append(line)
  return args
