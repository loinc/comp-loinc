from __future__ import annotations

import typing as t
from cProfile import label
from functools import reduce

from networkx.classes import edges

from comp_loinc.module import Module
from loinclib import Node, EdgeType, NodeType, GeneralProps
from loinclib.loinc_schema import LoincPartProps
from loinclib.loinc_tree_schema import LoincTreeProps

from urllib.parse import quote_plus


# from enum import StrEnum

class Groups:
  def __init__(self, module: Module):
    self.closured = None
    self.module = module

    self.groups: t.Dict[str, Group] = dict()
    self.properties: t.Dict[str, GroupProperty] = dict()
    self.parts: t.Dict[str, GroupPart] = dict()

    self.part_trees = {}
    self.property_trees = {}
    self.group_trees = {}

  def do_closure(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]):
    if self.closured:
      return

    self.closured = True

    for part in set(self.parts.values()):
      part.get_ancestors(part_parent_node_types=part_parent_node_types, part_parent_edge_types=part_parent_edge_types)

    for prop in set(self.properties.values()):
      prop.get_ancestors(part_parent_node_types=part_parent_node_types, part_parent_edge_types=part_parent_edge_types)

    for group in set(self.groups.values()):
      group.get_ancestors(part_parent_node_types=part_parent_node_types, part_parent_edge_types=part_parent_edge_types)

    for part in self.parts.values():
      parents = part.get_parents(part_parent_node_types=part_parent_node_types,
                                 part_parent_edge_types=part_parent_edge_types)
      if len(parents) == 0 and len(part.children) > 0:
        self.part_trees[part.key()] = part

    for prop in self.properties.values():
      parent = prop.get_parent(part_parent_node_types=part_parent_node_types,
                               part_parent_edge_types=part_parent_edge_types)
      if parent and len(prop.children) > 0:
        self.property_trees[prop.key()] = prop

    for group in self.groups.values():
      parent = group.get_parent(part_parent_node_types=part_parent_node_types,
                                part_parent_edge_types=part_parent_edge_types)
      if parent and len(group.children) > 0:
        self.group_trees[group.key()] = group


class Group:
  def __init__(self, groups_object: Groups):
    self._depth = None
    self._groups_object = groups_object
    self.__descendants_loincs_count = None
    self.__ancestors_loincs_count = None

    self.__descendants_count = None

    self.__depth = None

    self.loincs: t.Dict[str, Node] = dict()
    self._key = None

    self.properties: t.Dict[EdgeType, GroupProperty] = {}

    self.__parent: Group | t.Type[...] = ...
    self.children: t.Dict[str, Group] = {}
    self._ancestors: t.Dict[str, Group] | None = None

    self.from_loinc = False
    self.sources: t.Set[str] = set()

  def copy_properties(self) -> t.Dict[EdgeType, GroupProperty]:
    return dict(self.properties)

  def is_abstract(self):
    return len(self.loincs) == 0

  def is_complex(self):
    return len(self.properties) > 1

  def get_parent(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]) -> Group:
    if self.__parent is ...:
      properties = {}
      for edge, prop in self.properties.items():
        parent_prop = prop.get_parent(part_parent_node_types=part_parent_node_types,
                                      part_parent_edge_types=part_parent_edge_types)
        if parent_prop:
          parent_prop = self._groups_object.properties.setdefault(parent_prop.key(), parent_prop)
          properties[edge] = parent_prop
      if len(properties) > 0:
        parent_group = Group(groups_object=self._groups_object)
        parent_group.properties = properties
        parent_key = parent_group.key()
        if parent_key in self._groups_object.groups:
          parent_group = self._groups_object.groups[parent_key]
        else:
          self._groups_object.groups[parent_key] = parent_group
        self.__parent = parent_group
        if not self.from_loinc:
          parent_group.children[self.key()] = self
        parent_group.add_referrer_to_properties()
        parent_group.sources.update(self.sources)
      else:
        self.__parent = None
    return self.__parent

  def get_ancestors(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]) -> \
      t.Dict[str, Group]:
    if self._ancestors is None:
      self._ancestors = {}
      parent_group = self.get_parent(part_parent_node_types=part_parent_node_types,
                                     part_parent_edge_types=part_parent_edge_types)
      if parent_group:
        self._ancestors = {parent_group.key(): parent_group}
        self._ancestors.update(parent_group.get_ancestors(part_parent_node_types=part_parent_node_types,
                                                          part_parent_edge_types=part_parent_edge_types))
    return self._ancestors

  def get_descendants_loincs_count(self):
    count = 0
    for child in self.children.values():
      count += child.get_descendants_loincs_count()

    return count

  def get_descendants_count(self):
    if self.__descendants_count is None:
      self.__descendants_count = self._do_descendants_count(seen=[])
    return self.__descendants_count

  def _do_descendants_count(self, seen: t.List[Group]) -> int:
    if self in seen:
      seen.append(self)
      print("\n\nCount cycle =========")
      for g in seen:
        print(g.key())
      return 0
      raise ValueError(f"Group cycle: {[g.key() for g in seen]}")
    seen.append(self)
    count = len(self.children)
    for child in self.children.values():
      count += child._do_descendants_count(seen=list(seen))
    return count

  def get_ancestors_loincs_count(self):
    count = 0
    if self.__parent is not None and self.__parent is not ...:
      count = len(self.loincs) + self.__parent.get_ancestors_loincs_count()
    return count

  def get_group_depth(self):
    if self.__depth is None:
      self.__depth = 0
      if self.__parent is not None and self.__parent is not ...:
        self._depth = self.__parent.get_depth() + 1
    return self.__depth

  def __str__(self):
    string = f"Group:\n"
    for type_, prop in self.properties.items():
      string += f"{prop}\n"
    return string

  def has_concrete_child(self):
    return any([not child.is_abstract() for child in self.children.values()])

  def key(self) -> str:
    if self._key is not None:
      return self._key
    self._key = Group.build_key(self.properties)
    return self._key

  def add_referrer_to_properties(self):
    for prop in self.properties.values():
      prop.referring_groups[self.key()] = self

  @classmethod
  def build_key(cls, properties: t.Dict[EdgeType, GroupProperty]):
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
  def __init__(self, edge_type: EdgeType, parts: t.Set[GroupPart], groups_object: Groups):
    self.edge_type: EdgeType = edge_type
    self.parts: t.Set[GroupPart] = parts
    self._key = None
    self._groups_object: Groups = groups_object
    self.referring_groups: t.Dict[str, Group] = {}
    self.__parent: GroupProperty | t.Type[...] = ...
    self.children: t.Dict[str, GroupProperty] = {}
    self.ancestors: t.Dict[str, GroupProperty] = {}

    for part in parts:
      part.referring_properties[self.key()] = self

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

  def get_parent(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]):
    if self.__parent is ...:
      parent_parts: t.Dict[str, GroupPart] = {}
      for part in self.parts:
        parent_parts.update(part.get_parents(part_parent_node_types=part_parent_node_types,
                                             part_parent_edge_types=part_parent_edge_types))
      if len(parent_parts) > 0:
        parent_prop = GroupProperty(edge_type=self.edge_type,
                                    parts=set(parent_parts.values()),
                                    groups_object=self._groups_object)
        parent_prop = self._groups_object.properties.setdefault(parent_prop.key(), parent_prop)
        self.__parent = parent_prop
        parent_prop.children[self.key()] = self
        for parent_part in parent_parts.values():
          parent_part.referring_properties[parent_prop.key()] = parent_prop
      else:
        self.__parent = None
    return self.__parent

  def label(self):
    parts = list(self.parts)
    parts.sort(key=lambda x: x.key)
    _label = self.edge_type.value.label_fragment + " ".join([p.label() for p in parts])
    return _label

  def get_ancestors(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]) -> \
      t.Dict[
        str, GroupProperty]:
    if self.ancestors is None:
      self.ancestors = {}
      parent = self.get_parent(part_parent_node_types=part_parent_node_types,
                               part_parent_edge_types=part_parent_edge_types)
      if parent is not None:
        self.ancestors[parent.key()] = parent
        self.ancestors.update(parent.get_ancestors(part_parent_node_types=part_parent_node_types,
                                                   part_parent_edge_types=part_parent_edge_types))
    return self.ancestors

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
    self.__parents: t.Dict[str, GroupPart] | None = None
    self.children: t.Dict[str, GroupPart] = {}

    self.depth: float | None = None
    self.ancestors: t.Dict[str, GroupPart] | None = None
    self.referring_properties: t.Dict[str, GroupProperty] = {}

  def __eq__(self, other):
    return self.part_node == other.part_node

  def __hash__(self):
    return hash(GroupPart) ^ hash(self.part_node.node_id)

  def key(self):
    return self.part_node.node_id

  def get_parents(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]) -> \
      t.Dict[str, GroupPart]:

    if self.__parents is None:
      self.__parents = {}
      for parent_node in self.part_node.get_out_nodes(node_types=part_parent_node_types,
                                                      edge_types=part_parent_edge_types):
        parent = GroupPart(groups=self.groups, part_node=parent_node)
        parent = self.groups.parts.setdefault(parent.key(), parent)
        parent.children[self.key()] = self
        self.__parents[parent.key()] = parent
    return self.__parents

  def label(self):
    _label = ""
    _label += self.part_node.get_property(GeneralProps.label)
    # code = self.part_node.get_property(GeneralProps.code)
    # if code is None:
    #   print("debug")
    #   print(f"sources:{self.part_node.get_property(GeneralProps.sources)}", flush=True)
    _label += " " + self.part_node.get_property(GeneralProps.code)
    return _label

  def get_ancestors(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]) -> \
      t.Dict[
        str, GroupPart]:
    if self.ancestors is None:
      self.ancestors = {}
      for parent in self.get_parents(part_parent_node_types=part_parent_node_types,
                                     part_parent_edge_types=part_parent_edge_types).values():
        self.ancestors[parent.key()] = parent
        self.ancestors.update(parent.get_ancestors(part_parent_node_types=part_parent_node_types,
                                                   part_parent_edge_types=part_parent_edge_types))
    return self.ancestors

  def get_node_type(self) -> NodeType:
    return self.part_node.get_node_type()

  def get_key(self):
    return self.part_node.node_id

  def get_part_number(self):
    return self.part_node.get_property(GeneralProps.code)

  def get_depth(self, *, part_parent_node_types: t.List[NodeType], part_parent_edge_types: t.List[EdgeType]):
    if self.depth is None:
      parents = self.get_parents(part_parent_node_types=part_parent_node_types,
                                 part_parent_edge_types=part_parent_edge_types)
      self.depth = reduce(lambda d, p: d + p.get_depth(), parents, 1) / len(parents)
    return self.depth

  def get_depth_percent(self, *, other: GroupPart, part_parent_node_types: t.List[NodeType],
      part_parent_edge_types: t.List[EdgeType]):
    if self not in other.get_ancestors(part_parent_node_types=part_parent_node_types,
                                       part_parent_edge_types=part_parent_edge_types):
      raise ValueError(f"Group part: {other}, does not have this GroupPart as an ancestor: {self}")
    return self.depth / other.get_depth(part_parent_node_types=part_parent_node_types,
                                        part_parent_edge_types=part_parent_edge_types)

  def __str__(self):
    name = self.part_node.get_property(GeneralProps.label)
    # if name is None:
    #   name = f"TREE: {self.part_node.get_property(LoincTreeProps.code_text)}"
    return f"GroupPart: {name}  {self.part_node.node_id}"

  def name(self):
    name = self.part_node.get_property(GeneralProps.label)
    # if name is None:
    #   name = f"TREE: {self.part_node.get_property(LoincTreeProps.code_text)}"
    return f"{name}"
