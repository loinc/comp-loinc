from __future__ import annotations

import typing as t
from enum import StrEnum


class Property:
    def __init__(
        self, part_number: str, part_name: str, prop_type: t.Optional[StrEnum]
    ):
        self.count: int = 0
        self.part_number = part_number
        self.part_name = part_name
        self.prop_type = prop_type

        self.related_properties_by_key: t.Dict[str, Property] = {}
        self.related_properties_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}

        self.part_node: t.Optional[Part] = None

        self.child_prop_use_by_key: t.Dict[str, Property] = {}
        self.child_prop_use_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}

        self.parent_prop_use_by_key: t.Dict[str, Property] = {}
        self.parent_prop_use_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}

        self.depth: t.Optional[int] = None
        self.depth_percentage: t.Optional[float] = None

        self.descendants_count: t.Optional[int] = None

    def get_key(self):
        return f"{self.get_simple_property_name()}_{self.part_number}"

    def get_simple_property_name(self):
        s = str(self.prop_type)
        return s[s.rfind("/") + 1 :]

    def get_descendants_count(self, seen: set):
        if self in seen:
            return 0
        seen.add(self)
        if self.descendants_count is None:
            i = sum(
                [
                    c.get_descendants_count(seen)
                    for c in self.child_prop_use_by_key.values()
                ]
            )
            self.descendants_count = i + self.count
        return self.descendants_count

    def __str__(self):
        s = str(self.prop_type)
        return f"{self.get_simple_property_name()} -- {self.part_number} -- {self.part_name} -- #{self.count}"

    def __repr__(self):
        return self.__str__()

    def get_comp_related_systems_up(self, seen: set) -> t.Dict[str, Property]:
        if self.get_simple_property_name() != "COMPONENT":
            return {}
        if self in seen:
            return {}
        seen.add(self)
        systems = {}
        if "SYSTEM" in self.related_properties_by_name_key:
            return dict(self.related_properties_by_name_key["SYSTEM"])
        for parent in self.parent_prop_use_by_key.values():
            systems.update(parent.get_comp_related_systems_up(seen))
        return systems

    def get_abstracted(self, levels: int, seen: set) -> t.Dict[str, Property]:
        if self in seen:
            return {}
        seen.add(self)

        if self.count == 0 or levels == 1:
            return {self.get_key(): self}
        abstracts = {}
        for parent in self.parent_prop_use_by_key.values():
            # if parent.get_simple_property_name() == self.get_simple_property_name():
            abstracts.update(parent.get_abstracted(levels - 1, seen))
        return abstracts

    def get_top_concrete(self, levels: int, seen: set) -> t.Dict[str, Property]:
        if self in seen:
            return {}
        seen.add(self)
        if levels == 1:
            return {self.get_key(): self}
        concretes = {}
        for parent in self.parent_prop_use_by_key.values():
            if parent.count == 0:
                concretes[self.get_key()] = self
                continue
            concretes.update(self.get_top_concrete(levels - 1, seen))
        return concretes

    def abstract_to_more_than_count(
        self, count: int, seen: set
    ) -> t.Dict[str, Property]:
        if self in seen:
            return {}
        seen.add(self)
        abstract = {}
        if self.get_descendants_count(set()) > count:
            abstract = {self.get_key(): self}
        else:
            for parent in self.parent_prop_use_by_key.values():
                abstract.update(parent.abstract_to_more_than_count(count, seen))
        return abstract

    def parent_closure(self, seen: set) -> t.Dict[str, Property]:
        if self in seen:
            return {}
        seen.add(self)
        parents = {self.get_key(): self}
        for parent in self.parent_prop_use_by_key.values():
            parents.update(parent.parent_closure(seen))

        return parents


class Part:
    def __init__(
        self,
        part_number: str,
        part_name: t.Optional[str] = None,
        part_graph_id: t.Optional[str] = None,
    ):
        self.part_number: str = part_number
        self.part_display: str = part_name
        self.part_type: str = part_name
        self.part_graph_id: str = part_graph_id
        self.is_search: bool = False

        self.parents: t.Dict[str, Part] = {}
        self.children: t.Dict[str, Part] = {}

        self.property_by_key: t.Dict[str, Property] = {}
        self.property_by_name_key: t.Dict[str, t.Dict[str, Property]] = {}

    def __str__(self):
        return f"{self.part_type} -- {self.part_number} -- {self.part_display} -- #{len(self.property_by_key)} -- total #{sum([c.count for c in self.property_by_key.values()])}"
