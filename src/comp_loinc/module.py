import typing as t

import comp_loinc.datamodel.comp_loinc as v2
from comp_loinc.datamodel.comp_loinc import Entity


# class Modules:
#   def __init__(self, *,
#       graph: nx.MultiDiGraph = nx.MultiDiGraph(),
#       release_path: Path,
#       tree_path: Path = None,
#       loinc_version: str = None,
#   ):
#     self.module_map: t.Dict[str, Module] = dict()
#     self.graph: Graph = Graph(graph=graph,
#                               release_path=release_path,
#                               trees_path=tree_path,
#                               loinc_version=loinc_version,
#                               )


class Module:
  from comp_loinc import Runtime
  def __init__(self, *,
      name: str,
      runtime: Runtime
  ):
    from comp_loinc import Runtime
    self.name = name
    self.runtime: Runtime = runtime

    self.entities_by_type: t.Dict[
      t.Type[Entity], t.Dict[str, v2.Entity]] = dict()

    # flags for what to include
    self._include_loinc_long_common_name = None

  def get_entity(self, entity_id: str, entity_class: t.Type[Entity]) -> \
      t.Optional[Entity]:
    return self.entities_by_type.setdefault(entity_class, {}).get(entity_id,
                                                                  None)

  def add_entity(self, entity: Entity, replace: bool = False):
    if self.get_entity(entity.id, type(entity)) is not None and not replace:
      raise ValueError(f'Replacing entity {entity} not allowed.')
    self.entities_by_type.setdefault(type(entity), {})[entity.id] = entity

  def get_entities_of_type(self, entity_class: t.Type[Entity]) -> t.Iterator[Entity]:
    for entity in self.entities_by_type.get(entity_class, {}).values():
      yield entity

  def get_all_entities(self) -> t.Iterator[Entity]:
    for entity_map in self.entities_by_type.values():
      for entity in entity_map.values():
        yield entity

  # def create_loinc_terms_all(self):
  #   pass

  # def add_entity(self, entity: v2.Entity):
  #   self.__do_includes(entity)
  #
  # def include_loinc_term_long_common_names(self):
  #   if self._include_loinc_long_common_name:
  #     return
  #   self._include_loinc_long_common_name = True
  #   for loinc_term in self.entities.values():
  #     self.__do_includes(loinc_term)

  # def __do_includes(self, entity: v2.Entity):
  #   if isinstance(entity, v2.LoincTerm):
  #     self.__add_loinc_term_long_common_name(entity)

  # def __add_loinc_term_long_common_name(self, loinc_term: v2.LoincTerm):
  #   if not self._include_loinc_long_common_name:
  #     return
  #   name = self.modules.graph.get_first_node_property(
  #     property_key=PT.loinc_long_common_name)
  #   loinc_term.long_common_name = name
