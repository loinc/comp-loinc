from __future__ import annotations
import typing as t
from functools import reduce

from comp_loinc.module import Module
from loinclib import Node, EdgeType, GeneralEdgeType, NodeType
from loinclib.loinc_schema import LoincPartProps
from loinclib.loinc_tree_schema import LoincTreeProps

from urllib.parse import quote_plus

# from enum import StrEnum

class Groups:
  def __init__(self, module: Module):
    self.module = module
    self.groups: t.Dict[str, Group] = dict()
    self.roots: t.Dict[str, Group] = {}

    self.group_parts: t.Dict[str, GroupPart] = dict()


class Group:
  def __init__(self):
    self.__descendants_loincs_count = None
    self.__ancestors_loincs_count = None

    self.__descendants_count = None

    self.__depth = None

    self.loincs: t.Dict[str, Node] = dict()
    self._key = None

    self.parent_groups: t.Dict[str, Group] = dict()
    self.child_groups: t.Dict[str, Group] = dict()
    self.properties: t.Dict[EdgeType, t.Dict[str, GroupProperty]] = {}

    self.generated = False

  def copy(self) -> Group:
    copy = Group()
    copy.loincs = dict(self.loincs)
    copy.parent_groups = dict(self.parent_groups)
    copy.child_groups = dict(self.child_groups)
    copy.properties = dict(self.properties)
    copy.generated = self.generated
    return copy

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
    for type_, group_properties in self.properties.items():
      for key, group_property in group_properties.items():
        string += f"{group_property}\n"
    return string

  def has_concrete_child(self):
    return any([not child.is_abstract() for child in self.child_groups.values()])

  def key(self) -> str:
    if self._key is not None:
      return self._key

    group_key: t.Optional[str] = None
    prop_type: EdgeType

    property_types = list(self.properties.keys())
    property_types.sort(key=lambda x: x.name)
    for prop_type in property_types:
      type_prefix = prop_type.name + "_"
      if group_key is None:
        group_key = type_prefix
      else:
        group_key += "--" + type_prefix

      group_properties = self.properties[prop_type]
      keys =  list(group_properties.keys())
      keys.sort()

      for key in keys:
        group_property = group_properties[key]

        part_node = group_property.group_part.part_node
        name = part_node.get_property(LoincPartProps.part_name)
        if name is None:
            name = f"TREE: {part_node.get_property(LoincTreeProps.code_text)}"

        group_key += name + "_"
        group_key += group_property.group_part.part_node.get_property(LoincPartProps.part_number) + "_"
        group_key = quote_plus(group_key)
    self._key = group_key
    return self._key


class GroupProperty:
  def __init__(self, edge_type: EdgeType, group_part: GroupPart):
    self.edge_type: EdgeType = edge_type
    self.group_part: GroupPart = group_part

  def __eq__(self, other):
    return self.edge_type == other.edge_type and self.group_part == other.group_part

  def __hash__(self):
    return hash((self.edge_type, self.group_part.part_node.node_id))

  def __str__(self):
    return f"GroupProperty: {self.edge_type.name}: {self.group_part}"

  def key(self):
    return f"{self.edge_type.name}:{self.group_part.key()}"

  def name(self):
    return f""


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

  def get_parents(self, *parent_types: NodeType) -> t.Set[GroupPart]:
    if self.parents is None:
      self.parents = set()
      for parent_node in self.part_node.get_out_nodes(*parent_types):
        self.parents.add(self.groups.group_parts.setdefault(parent_node.node_id, GroupPart(groups=self.groups, part_node=parent_node)))
    return self.parents

  def get_ancestors(self, *ancestor_types: NodeType) -> t.Set[GroupPart]:
    if self.ancestors is None:
      self.ancestors = set()
      self.ancestors.add(self)
      for parent in self.get_parents(*ancestor_types):
        self.ancestors.update(parent.get_ancestors(*ancestor_types))
    return self.ancestors

  def get_node_type(self):
    return self.part_node.get_node_type()

  def get_key(self):
    return self.part_node.node_id

  def get_depth(self):
    if self.depth is None:
      parents = self.get_parents()
      self.depth = reduce(lambda d, p: d + p.get_depth(), parents, 1) / len(parents)
    return self.depth

  def get_depth_percent(self, other: GroupPart):
    if self not in other.get_ancestors():
      raise ValueError(f"Group part: {other}, does not have this GroupPart as an ancestor: {self}")
    return self.depth / other.get_depth()

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
