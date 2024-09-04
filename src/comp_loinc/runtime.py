import logging
import sys
import typing as t
from logging import Logger
from pathlib import Path

import linkml_runtime
from linkml_runtime import SchemaView

from loinclib import LoinclibGraph
from loinclib.config import Configuration


class Runtime:
  def __init__(self, *,
      name: str = 'default',
      pickled_graph_path: Path = None,
      configuration: Configuration):
    self.configuration = configuration
    self.name = name
    self.pickled_graph_path = pickled_graph_path

    self.graph = LoinclibGraph(graph_path=self.pickled_graph_path)

    from comp_loinc.module import Module
    self.modules: t.Dict[str, Module] = dict()
    self.current_module: t.Optional[Module] = None

    self.schema_views: t.Dict[str, SchemaView] = dict()
    self.current_schema_view: t.Optional[SchemaView] = None

    self.logger: Logger = logging.getLogger(f'{self.name}_runtime')

  def load_linkml_schema(self, file_name: str, as_name: str = None, reload: bool = False) -> SchemaView:
    from comp_loinc import schemas_path
    if as_name is None:
      as_name = file_name.removesuffix('.yaml')

    current_view = self.schema_views.get(as_name, None)
    if current_view and not reload:
      file = current_view.schema.source_file
      raise ValueError(f'Schema view for name: {as_name} already loaded from file: {file}')

    schema_path = schemas_path / file_name
    if schema_path.exists():
      schema_view = linkml_runtime.SchemaView(schema_path)
      self.schema_views[as_name] = schema_view
      return schema_view
    else:
      raise ValueError(f'Schema file {schema_path} does not exist while trying to load as name: {as_name}')
