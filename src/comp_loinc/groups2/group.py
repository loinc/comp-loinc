import typing as t

from loinclib import Node, EdgeType
from loinclib.loinc_schema import LoincPartProps
from loinclib.loinc_tree_schema import LoincTreeProps


# from enum import StrEnum


class Group:
  def __init__(self):
    self.properties: t.Dict[EdgeType, Node] = dict()
    self.loincs: t.Dict[str, Node] = dict()
    self.key = None

    self.parent_groups: t.Dict[str, Group] = dict()
    self.child_groups: t.Dict[str, Group] = dict()

  def get_key(self):
    if self.key is None:
      self.key = Group.group_key(self.properties)
    return self.key

  def is_abstract(self):
    return len(self.loincs) == 0

  def is_complex(self):
    return len(self.properties) > 1

  def __repr__(self):
    string = f"{self.key}"
    for type_, node in self.properties.items():
      name = node.get_property(LoincPartProps.part_name)
      if name is None:
        name = f"TREE: {node.get_property(LoincTreeProps.code_text)}"

      string += f" -- {type_.value.abbr}  {name}"
    return string

  def __str__(self):
    return self.__repr__()

  @classmethod
  def group_key(cls, properties: t.Dict[EdgeType, Node]):
    group_key: t.Optional[str] = None
    for prop, part_node in properties.items():
      prefix = prop.value.abbr
      part_name = part_node.get_property(LoincPartProps.part_name)
      part_number = part_node.get_property(LoincPartProps.part_number)
      if group_key is None:
        group_key = f"{prefix}:{part_number}"
      else:
        group_key = group_key + f"|{prefix}:{part_number}"

    return group_key
