from __future__ import annotations

import typing as t
from functools import reduce

from networkx.classes import edges

from comp_loinc.module import Module
from loinclib import Node, EdgeType, NodeType
from loinclib.loinc_schema import LoincPartProps
from loinclib.loinc_tree_schema import LoincTreeProps

from urllib.parse import quote_plus


# from enum import StrEnum

class Groups:
  def __init__(self, module: Module):
    self.module = module

    self.roots: t.Dict[str, Group] = {}

    self.groups: t.Dict[str, Group] = dict()
    self.properties: t.Dict[str, GroupProperty] = dict()
    self.parts: t.Dict[str, GroupPart] = dict()


class Group:
  def __init__(self, groups: Groups):
    self.groups = groups
    self.__descendants_loincs_count = None
    self.__ancestors_loincs_count = None

    self.__descendants_count = None

    self.__depth = None

    self.loincs: t.Dict[str, Node] = dict()
    self._key = None

    self.parent_groups: t.Dict[str, Group] = dict()
    self.child_groups: t.Dict[str, Group] = dict()
    self.properties: t.Dict[EdgeType, GroupProperty] = {}

    self.generated = False

  def copy_properties(self) -> t.Dict[EdgeType, GroupProperty]:
    return dict(self.properties)

  def is_abstract(self):
    return len(self.loincs) == 0

  def is_complex(self):
    return len(self.properties) > 1

  def get_descendants_loincs_count(self):
    if self.__descendants_loincs_count is None:
      self.__descendants_loincs_count = self._do_descendant_loincs_count(set())
    return self.__descendants_loincs_count

  def get_descendants_count(self):
    if self.__descendants_count is None:
      self.__descendants_count = self._do_descencents_count(self, set())
    return self.__descendants_count

  def _do_descencents_count(self, group: Group, seen: set):
    count = 1
    if self.key() in seen:
      return count
    seen.add(self.key())
    for key, child in self.child_groups.items():
      count += self._do_descencents_count(child, seen)
    return count

  def _do_descendant_loincs_count(self, seen_keys: set):
    count = len(self.loincs)
    seen_keys.add(self.key())

    for key, child in self.child_groups.items():
      if key in seen_keys:
        continue
      count += child._do_descendant_loincs_count(seen_keys)
    return count

  def get_ancestors_loincs_count(self):
    if self.__ancestors_loincs_count is None:
      self.__ancestors_loincs_count = self._do_ancestors_loincs_count(set())
    return self.__ancestors_loincs_count

  def _do_ancestors_loincs_count(self, seen_keys: set):
    count = len(self.loincs)
    seen_keys.add(self.key())
    for key, parent in self.parent_groups.items():
      if key in seen_keys:
        continue
      count += parent._do_ancestors_loincs_count(seen_keys)
    return count

  def get_group_depth(self):
    if self.__depth is None:
      self.__depth = self._do_depth(set())
    return self.__depth

  def _do_depth(self, seen_keys: set):
    depth = 0
    seen_keys.add(self.key())
    for key, group in self.parent_groups.items():
      if key in seen_keys:
        continue
      seen_keys.add(key)
      depth = max(depth, group._do_depth(seen_keys))
    return depth

  def __str__(self):
    string = f"Group:\n"
    for type_, prop in self.properties.items():
        string += f"{prop}\n"
    return string

  def has_concrete_child(self):
    return any([not child.is_abstract() for child in self.child_groups.values()])

  def key(self) -> str:
    if self._key is not None:
      return self._key
    self._key = Group.build_key(self.properties)
    return self._key

  @classmethod
  def build_key(cls, properties:t.Dict[EdgeType, GroupProperty]):
    group_key = None
    edge: EdgeType

    edge_types = list(properties.keys())
    edge_types.sort(key=lambda x: x.name)
    for edge in edge_types:
      type_prefix = edge.name + ":"
      if group_key is None:
        group_key = type_prefix
      else:
        group_key += "--" + type_prefix

      group_key += properties[edge].key()
    return group_key


class GroupProperty:
  def __init__(self, edge_type: EdgeType, group_parts: t.Set[GroupPart], groups: Groups):
    self.edge_type: EdgeType = edge_type
    self.parts: t.Set[GroupPart] = group_parts
    self._key = None
    self.groups: Groups = groups
    self.parent = ...
    self.children: t.Dict[str, GroupProperty] = {}

  def __eq__(self, other):
    return self.edge_type == other.edge_type and self.parts == other.parts

  def __hash__(self):
    hsh = hash(self.edge_type)
    for part in self.parts:
      hsh ^= hash(part)
    return hsh

  def __str__(self):
    return f"GroupProperty: {self.edge_type.name}: {self.parts}"

  def key(self):
    if self._key is None:
      _key = f"{self.edge_type.name}:"
      for part in self.parts:
        _key += f"_{part.key()}"
      self._key = _key
    return self._key

  def name(self):
    return f""

  def get_parent_property(self, *, parent_node_types: t.List[NodeType], edge_types: t.List[EdgeType]):
    if self.parent is not ...:
      return self.parent

    for part in self.parts:
      parent_parts = part.get_parents(parent_node_types=parent_node_types, edge_types=edge_types)
      if len(parent_parts) > 0:
        key = GroupProperty.property_key(edge_type=self.edge_type, parts=parent_parts)
        self.parent = self.groups.properties.setdefault(key, GroupProperty(edge_type=self.edge_type,
                                                                           group_parts=parent_parts,
                                                                           groups=self.groups))
        self.parent.children[self.key()] = self
      else:
        self.parent = None
    return self.parent

  @classmethod
  def property_key(cls, edge_type: EdgeType, parts: t.Set[GroupPart]):
    key = f"{edge_type.name}:"
    parts: t.List[GroupPart] = list(parts)
    parts.sort(key=lambda x: x.key())
    for part in parts:
      key += f"_{part.key()}"
    return key


class GroupPart:
  def __init__(self, *, groups: Groups, part_node: Node):
    self.part_node: Node = part_node
    self.groups = groups
    self.parents: t.Set[GroupPart] | None = None
    self.depth: float | None = None
    self.ancestors: t.Set[GroupPart] | None = None
    self.group_properties: t.List[GroupProperty] = []

  def __eq__(self, other):
    return self.part_node == other.part_node

  def __hash__(self):
    return hash(GroupPart) ^ hash(self.part_node.node_id)

  def key(self):
    return self.part_node.node_id

  def get_parents(self, *, parent_node_types: t.List[NodeType], edge_types: t.List[EdgeType]) -> t.Set[GroupPart]:
    if self.parents is None:
      self.parents = set()
      for parent_node in self.part_node.get_out_nodes(node_types=parent_node_types, edge_types=edge_types):
        parent_part = GroupPart(groups=self.groups, part_node=parent_node)
        self.parents.add(
            self.groups.parts.setdefault(parent_part.key(), parent_part))
    return self.parents

  def get_ancestors(self, *, parent_node_types: t.List[NodeType], edge_types: t.List[EdgeType]) -> t.Set[GroupPart]:
    if self.ancestors is None:
      self.ancestors = set()
      self.ancestors.add(self)
      for parent in self.get_parents(parent_node_types=parent_node_types, edge_types=edge_types):
        self.ancestors.update(parent.get_ancestors(parent_node_types=parent_node_types, edge_types=edge_types))
    return self.ancestors

  def get_node_type(self) -> NodeType:
    return self.part_node.get_node_type()

  def get_key(self):
    return self.part_node.node_id

  def get_depth(self, *, parent_node_types: t.List[NodeType], edge_types: t.List[EdgeType]):
    if self.depth is None:
      parents = self.get_parents(parent_node_types=parent_node_types, edge_types=edge_types)
      self.depth = reduce(lambda d, p: d + p.get_depth(), parents, 1) / len(parents)
    return self.depth

  def get_depth_percent(self, *, other: GroupPart, parent_node_types: t.List[NodeType], edge_types: t.List[EdgeType]):
    if self not in other.get_ancestors(parent_node_types=parent_node_types, edge_types=edge_types):
      raise ValueError(f"Group part: {other}, does not have this GroupPart as an ancestor: {self}")
    return self.depth / other.get_depth(parent_node_types=parent_node_types, edge_types=edge_types)

  def __str__(self):
    name = self.part_node.get_property(LoincPartProps.part_name)
    if name is None:
      name = f"TREE: {self.part_node.get_property(LoincTreeProps.code_text)}"
    return f"GroupPart: {name}  {self.part_node.node_id}"

  def name(self):
    name = self.part_node.get_property(LoincPartProps.part_name)
    if name is None:
      name = f"TREE: {self.part_node.get_property(LoincTreeProps.code_text)}"
    return f"GP {name} {self.part_node.node_id}"
