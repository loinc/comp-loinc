from __future__ import annotations

import typing as t
from enum import StrEnum


class PropertyUse:
  def __init__(self, part_number: str, part_name: str, prop_type: t.Optional[StrEnum]):
    self.count: int = 0
    self.part_number = part_number
    self.part_name = part_name
    self.prop_type = prop_type

    self.related_props_by_key: t.Dict[str, PropertyUse] = {}
    self.related_props_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}

    self.part_node: t.Optional[PartNode] = None

    self.child_prop_use_by_key: t.Dict[str, PropertyUse] = {}
    self.child_prop_use_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}

    self.parent_prop_use_by_key: t.Dict[str, PropertyUse] = {}
    self.parent_prop_use_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}

  def get_key(self):
    return f'{self.get_simple_property_name()}_{self.part_number}'

  def get_simple_property_name(self):
    s = str(self.prop_type)
    return s[s.rfind("/")+1:]

  def __str__(self):
    s = str(self.prop_type)
    return f'{self.get_simple_property_name()} -- {self.part_number} -- {self.part_name} -- #{self.count}'


class PartNode:
  def __init__(self, part_number: str, part_name: t.Optional[str] = None, part_graph_id: t.Optional[str] = None):
    self.part_number: str = part_number
    self.part_name: str = part_name
    self.part_type_name: str = part_name
    self.part_graph_id: str = part_graph_id
    self.is_search: bool = False

    self.parents: t.Dict[str, PartNode] = {}
    self.children: t.Dict[str, PartNode] = {}

    self.prop_use_by_key: t.Dict[str, PropertyUse] = {}
    self.prop_use_by_name_key: t.Dict[str, t.Dict[str, PropertyUse]] = {}


  def __str__(self):
    return f'{self.part_type_name} -- {self.part_number} -- {self.part_name} -- #{len(self.prop_use_by_key)} -- total #{sum([c.count for c in self.prop_use_by_key.values()])}'