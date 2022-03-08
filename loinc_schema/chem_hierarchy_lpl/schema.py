# Auto generated from schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-02-24T09:47:21
# Schema: chemicalinfo
#
# id: https://w3id.org/linkml/examples/chemicalinfo
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
import sys
import re
from jsonasobj2 import JsonObj, as_dict
from typing import Optional, List, Union, Dict, ClassVar, Any
from dataclasses import dataclass
from linkml_runtime.linkml_model.meta import EnumDefinition, PermissibleValue, PvFormulaOptions

from linkml_runtime.utils.slot import Slot
from linkml_runtime.utils.metamodelcore import empty_list, empty_dict, bnode
from linkml_runtime.utils.yamlutils import YAMLRoot, extended_str, extended_float, extended_int
from linkml_runtime.utils.dataclass_extensions_376 import dataclasses_init_fn_with_kwargs
from linkml_runtime.utils.formatutils import camelcase, underscore, sfx
from linkml_runtime.utils.enumerations import EnumDefinitionImpl
from rdflib import Namespace, URIRef
from linkml_runtime.utils.curienamespace import CurieNamespace
from linkml_runtime.linkml_model.types import String

metamodel_version = "1.7.0"

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LOINC = CurieNamespace('LOINC', 'https://loinc.org/')
CHEMICALINFO = CurieNamespace('chemicalinfo', 'https://w3id.org/linkml/examples/chemicalinfo/')
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = CHEMICALINFO


# Types

# Class references
class LOINCLOINCId(extended_str):
    pass


@dataclass
class LOINC(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHEMICALINFO.LOINC
    class_class_curie: ClassVar[str] = "chemicalinfo:LOINC"
    class_name: ClassVar[str] = "LOINC"
    class_model_uri: ClassVar[URIRef] = CHEMICALINFO.LOINC

    LOINCId: Union[str, LOINCLOINCId] = None
    LOINCCode: str = None
    LOINCName: str = None
    has_part: Optional[Union[Union[dict, "Part"], List[Union[dict, "Part"]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.LOINCId):
            self.MissingRequiredField("LOINCId")
        if not isinstance(self.LOINCId, LOINCLOINCId):
            self.LOINCId = LOINCLOINCId(self.LOINCId)

        if self._is_empty(self.LOINCCode):
            self.MissingRequiredField("LOINCCode")
        if not isinstance(self.LOINCCode, str):
            self.LOINCCode = str(self.LOINCCode)

        if self._is_empty(self.LOINCName):
            self.MissingRequiredField("LOINCName")
        if not isinstance(self.LOINCName, str):
            self.LOINCName = str(self.LOINCName)

        if not isinstance(self.has_part, list):
            self.has_part = [self.has_part] if self.has_part is not None else []
        self.has_part = [v if isinstance(v, Part) else Part(**as_dict(v)) for v in self.has_part]

        super().__post_init__(**kwargs)


@dataclass
class Part(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHEMICALINFO.Part
    class_class_curie: ClassVar[str] = "chemicalinfo:Part"
    class_name: ClassVar[str] = "Part"
    class_model_uri: ClassVar[URIRef] = CHEMICALINFO.Part

    PartCode: str = None
    PartName: str = None
    part_type: Optional[Union[Union[dict, "PartType"], List[Union[dict, "PartType"]]]] = empty_list()
    part_of: Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.PartCode):
            self.MissingRequiredField("PartCode")
        if not isinstance(self.PartCode, str):
            self.PartCode = str(self.PartCode)

        if self._is_empty(self.PartName):
            self.MissingRequiredField("PartName")
        if not isinstance(self.PartName, str):
            self.PartName = str(self.PartName)

        if not isinstance(self.part_type, list):
            self.part_type = [self.part_type] if self.part_type is not None else []
        self.part_type = [v if isinstance(v, PartType) else PartType(**as_dict(v)) for v in self.part_type]

        self._normalize_inlined_as_list(slot_name="part_of", slot_type=LOINC, key_name="LOINCId", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class PartType(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHEMICALINFO.PartType
    class_class_curie: ClassVar[str] = "chemicalinfo:PartType"
    class_name: ClassVar[str] = "PartType"
    class_model_uri: ClassVar[URIRef] = CHEMICALINFO.PartType

    PartTypeCode: str = None
    PartTypeName: str = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.PartTypeCode):
            self.MissingRequiredField("PartTypeCode")
        if not isinstance(self.PartTypeCode, str):
            self.PartTypeCode = str(self.PartTypeCode)

        if self._is_empty(self.PartTypeName):
            self.MissingRequiredField("PartTypeName")
        if not isinstance(self.PartTypeName, str):
            self.PartTypeName = str(self.PartTypeName)

        super().__post_init__(**kwargs)


@dataclass
class Container(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = CHEMICALINFO.Container
    class_class_curie: ClassVar[str] = "chemicalinfo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = CHEMICALINFO.Container

    LOINCData: Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="LOINCData", slot_type=LOINC, key_name="LOINCId", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LOINCId = Slot(uri=CHEMICALINFO.LOINCId, name="LOINCId", curie=CHEMICALINFO.curie('LOINCId'),
                   model_uri=CHEMICALINFO.LOINCId, domain=None, range=URIRef)

slots.LOINCCode = Slot(uri=CHEMICALINFO.LOINCCode, name="LOINCCode", curie=CHEMICALINFO.curie('LOINCCode'),
                   model_uri=CHEMICALINFO.LOINCCode, domain=None, range=str)

slots.LOINCName = Slot(uri=CHEMICALINFO.LOINCName, name="LOINCName", curie=CHEMICALINFO.curie('LOINCName'),
                   model_uri=CHEMICALINFO.LOINCName, domain=None, range=str)

slots.has_part = Slot(uri=CHEMICALINFO.has_part, name="has_part", curie=CHEMICALINFO.curie('has_part'),
                   model_uri=CHEMICALINFO.has_part, domain=None, range=Optional[Union[Union[dict, Part], List[Union[dict, Part]]]])

slots.PartCode = Slot(uri=CHEMICALINFO.PartCode, name="PartCode", curie=CHEMICALINFO.curie('PartCode'),
                   model_uri=CHEMICALINFO.PartCode, domain=None, range=str)

slots.PartName = Slot(uri=CHEMICALINFO.PartName, name="PartName", curie=CHEMICALINFO.curie('PartName'),
                   model_uri=CHEMICALINFO.PartName, domain=None, range=str)

slots.part_type = Slot(uri=CHEMICALINFO.part_type, name="part_type", curie=CHEMICALINFO.curie('part_type'),
                   model_uri=CHEMICALINFO.part_type, domain=None, range=Optional[Union[Union[dict, PartType], List[Union[dict, PartType]]]])

slots.part_of = Slot(uri=CHEMICALINFO.part_of, name="part_of", curie=CHEMICALINFO.curie('part_of'),
                   model_uri=CHEMICALINFO.part_of, domain=None, range=Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]])

slots.PartTypeCode = Slot(uri=CHEMICALINFO.PartTypeCode, name="PartTypeCode", curie=CHEMICALINFO.curie('PartTypeCode'),
                   model_uri=CHEMICALINFO.PartTypeCode, domain=None, range=str)

slots.PartTypeName = Slot(uri=CHEMICALINFO.PartTypeName, name="PartTypeName", curie=CHEMICALINFO.curie('PartTypeName'),
                   model_uri=CHEMICALINFO.PartTypeName, domain=None, range=str)

slots.LOINCData = Slot(uri=CHEMICALINFO.LOINCData, name="LOINCData", curie=CHEMICALINFO.curie('LOINCData'),
                   model_uri=CHEMICALINFO.LOINCData, domain=None, range=Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]])
