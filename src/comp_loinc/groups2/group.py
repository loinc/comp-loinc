import typing as t
from enum import StrEnum

from loinclib import Node, LoincNodeType
from loinclib.loinc_schema import LoincPartProps


class Group:
  def __init__(self):
    self.properties: t.Dict[StrEnum, Node] = dict()
    self.loincs: t.Dict[str, Node] = dict()
    self.key = None

    self.parent_groups: t.Dict[str, Group] = dict()
    self.child_groups: t.Dict[str, Group] = dict()

  def get_key(self):
    if self.key is None:
      self.key = Group.group_key(self.properties)
    return self.key

  @classmethod
  def group_key(cls, properties):
    key: str = None
    for k, v in properties.items():
      prefix = k.prefix
      part_name = v.get_property(LoincPartProps.part_name)
      part_number = v.get_property(LoincPartProps.part_number)
      if key is None:
        key = f"{prefix}:{part_number}"
      else:
        key = key + f"|{prefix}:{part_number}"

    return key