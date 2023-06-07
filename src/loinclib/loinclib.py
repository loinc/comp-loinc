from __future__ import annotations

import pathlib
import typing
from dataclasses import dataclass

import pandas as pd


@dataclass
class Mapping:
    code: str
    display: str
    system: str
    mapping: str


class LoincEntity:

    def __init__(self,
                 code: str):
        self.code: str = code

        self.component_hierarchy_text: typing.Optional[str] = None
        self.component_hierarchy_sequence: typing.Optional[str] = None

        self.part_type: typing.Optional[str] = None
        self.part_name: typing.Optional[str] = None
        self.part_display: typing.Optional[str] = None
        self.part_status: typing.Optional[str] = None

        self.parents: typing.Set[LoincEntity] = set()
        self.children: typing.Set[LoincEntity] = set()

    def __eq__(self, other):
        if isinstance(other, LoincEntity):
            return self.code == other.code
        return False

    def __hash__(self):
        return self.code.__hash__()

    def is_part(self):
        return self.code.startswith('LP')


class LoincRelease:

    def __init__(self, directory: pathlib.Path, version: str):
        self.directory: pathlib.Path = directory
        self.version: str = version
        # self.frame_caching: bool = frame_caching

        self.__entity_map: typing.Dict[str, LoincEntity] = {}

        # self.__loinc_frame: pd.DataFrame | None = None
        # self.__loinc_part_link_primary_frame: pd.DataFrame | None = None
        # self.__loinc_part_link_supplementary_frame: pd.DataFrame | None = None
        #
        # self.__part_frame: pd.DataFrame | None = None
        # self.__part_related_code_mapping_frame: pd.DataFrame | None = None
        #
        # self.__component_hierarchy_by_system_frame: pd.DataFrame | None = None

        # self.__parts_parents: typing.Dict[str, typing.Set] | None = None

        # self.__codes_map: typing.Dict[str, Code] = {}

    def parse_component_hierarchy_by_system(self):
        tuples = self.component_hierarchy_by_system_frame().itertuples()

        for t in tuples:
            path: str = t.PATH_TO_ROOT
            sequence: str = t.SEQUENCE
            immediate_parent: str = t.IMMEDIATE_PARENT
            code: str = t.CODE
            code_text: str = t.CODE_TEXT

            parent = self.__entity_map.setdefault(immediate_parent, LoincEntity(immediate_parent)) \
                if immediate_parent else None

            child = self.__entity_map.setdefault(code, LoincEntity(code))
            child.component_hierarchy_text = code_text

            if parent:
                parent.children.add(child)
                child.parents.add(parent)

    def parse_parts(self):
        itertuples = self.part_frame().itertuples()
        for t in itertuples:
            code = t.PartNumber
            part_type = t.PartTypeName
            part_name = t.PartName
            part_display = t.PartDisplayName
            status = t.Status

            part = self.__entity_map.setdefault(code, LoincEntity(code))
            part.part_type = part_type
            part.part_name = part_name
            part.part_display = part_display
            part.part_status = status

    def parts(self) -> typing.Dict[str, LoincEntity]:
        return {code: entity for (code, entity) in self.__entity_map.items() if entity.is_part()}

    #######################
    # Frames
    #######################

    def loinc_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'LoincTable' / 'Loinc.csv', dtype=str, na_filter=False)

    def component_hierarchy_by_system_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'AccessoryFiles' / 'ComponentHierarchyBySystem' /
                           'ComponentHierarchyBySystem.csv', dtype=str, na_filter=False)

    def loinc_part_link_primary_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Primary.csv', dtype=str,
                           na_filter=False)

    def loinc_part_link_supplementary_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Supplementary.csv',
                           dtype=str, na_filter=False)

    def part_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'AccessoryFiles' / 'PartFile' / 'Part.csv', dtype=str, na_filter=False)

    def part_related_code_mapping_frame(self) -> pd.DataFrame:
        return pd.read_csv(self.directory / 'AccessoryFiles' / 'PartFile' / 'PartRelatedCodeMapping.csv', dtype=str,
                           na_filter=False)

    #
    # def parts_parents(self, cache: bool = False):
    #     if self.__parts_parents:
    #         return self.__parts_parents
    #     parts_parents: typing.Dict[str, typing.Set] = {}
    #     frame = self.component_hierarchy_by_system_frame()
    #     for t in frame.itertuples():
    #         code: str = getattr(t, 'CODE')
    #         parent: str = getattr(t, 'IMMEDIATE_PARENT')
    #         if code.startswith('LP'):
    #             parents: typing.Set = parts_parents.setdefault(code, set())
    #             parents.add(parent)
    #     if cache:
    #         self.__parts_parents = parts_parents
    #     return parts_parents


#
# def load_loinc_frame(directory: pathlib.Path, version: str) -> pd.DataFrame:
#     return pd.read_csv(directory / 'LoincTable' / 'Loinc.csv', dtype=str)
#
#
# # Parts
# def load_part_frame(directory: pathlib.Path, version: str) -> pd.DataFrame:
#
#
#
# def load_loinc_part_link_primary_frame(directory: pathlib.Path, version: str) -> pd.DataFrame:
#
#
#
# def load_loinc_part_link_supplementary_frame(directory: pathlib.Path, version: str) -> pd.DataFrame:
#
#
#
# def load_part_related_code_mapping_frame(directory: pathlib.Path, version: str) -> pd.DataFrame:
#


if __name__ == '__main__':
    main_loinc_release = LoincRelease(pathlib.Path('data/loinc_release/extracted'), '2.7.4')
    main_parts_parents = main_loinc_release.parts_parents()
    print(len(main_parts_parents))
