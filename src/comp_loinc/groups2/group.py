from __future__ import annotations
import typing as t

from loinclib import Node, EdgeType
from loinclib.loinc_schema import LoincPartProps
from loinclib.loinc_tree_schema import LoincTreeProps


# from enum import StrEnum


class Group:
    def __init__(self):
        self.__descendants_loincs_count = None
        self.__ancestors_loincs_count = None

        self.__descendants_count = None

        self.__depth = None

        self.loincs: t.Dict[str, Node] = dict()
        self.key = None

        self.parent_groups: t.Dict[str, Group] = dict()
        self.child_groups: t.Dict[str, Group] = dict()

        self.properties: t.Dict[EdgeType, t.Set[GroupProperty]] = {}

    def get_key(self):
        if self.key is None:
            self.key = self.group_key()
        return self.key

    def is_abstract(self):
        return len(self.loincs) == 0

    def is_complex(self):
        return len(self.properties) > 1

    def __repr__(self):
        string = f"{self.key}"
        for type_, group_properties in self.properties.items():
            for group_property in group_properties:
                node = group_property.group_part.part_node
                name = node.get_property(LoincPartProps.part_name)
                if name is None:
                    name = f"TREE: {node.get_property(LoincTreeProps.code_text)}"

                string += f" -- {type_.value.abbr}  {name}"
        return string

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
        if self.key in seen:
            return count
        seen.add(self.key)
        for key, child in self.child_groups.items():
            count += self._do_descencents_count(child, seen)
        return count

    def _do_descendant_loincs_count(self, seen_keys: set):
        count = len(self.loincs)
        seen_keys.add(self.get_key())

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
        seen_keys.add(self.get_key())
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
        seen_keys.add(self.get_key())
        for key, group in self.parent_groups.items():
            if key in seen_keys:
                continue
            seen_keys.add(key)
            depth = max(depth, group._do_depth(seen_keys))
        return depth

    def __str__(self):
        return self.__repr__()

    def has_concrete_child(self):
        return any([not child.is_abstract() for child in self.child_groups.values()])

    def group_key(self) -> str:
        if self.key is not None:
            return self.key

        group_key: t.Optional[str] = None
        prop_type: EdgeType

        property_types = list(self.properties.keys())
        property_types.sort(key=lambda x: x.value.name)
        for prop_type in property_types:
            type_prefix = prop_type.value.abbr + "_"
            if group_key is None:
                group_key = type_prefix
            else:
                group_key += "--" + type_prefix


            group_properties = self.properties[prop_type]

            for group_property in group_properties:
                group_key += group_property.group_part.part_node.get_property(LoincPartProps.part_name) + "_"
                group_key += group_property.group_part.part_node.get_property(LoincPartProps.part_number) + "_"
        self.key = group_key
        return self.key


class GroupProperty:
    def __init__(self, edge_type: EdgeType, group_part: GroupPart):
        self.edge_type: EdgeType = edge_type
        self.group_part: GroupPart = group_part

    def __eq__(self, other):
        return self.edge_type == other.edge_type and self.group_part == other.group_part

    def __hash__(self):
        return hash((self.edge_type, self.group_part.part_node.node_id))

class GroupPart:
    def __init__(self, part_node: Node):
        self.part_node: Node = part_node

    def __eq__(self, other):
        return self.part_node == other.part_node
