# Auto generated from loincinfo.yaml by pythongen.py version: 0.9.0
# Generation date: 2021-12-02T10:22:22
# Schema: loincinfo
#
# id: https://w3id.org/linkml/examples/loincinfo
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
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOINCINFO = CurieNamespace('loincinfo', 'https://w3id.org/linkml/examples/loincinfo/')
SCHEMA = CurieNamespace('schema', 'http://schema.org/')
DEFAULT_ = LOINCINFO


# Types

# Class references
class LOINCLOINCId(extended_str):
    pass


@dataclass
class LOINC(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINCINFO.LOINC
    class_class_curie: ClassVar[str] = "loincinfo:LOINC"
    class_name: ClassVar[str] = "LOINC"
    class_model_uri: ClassVar[URIRef] = LOINCINFO.LOINC

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

        self._normalize_inlined_as_list(slot_name="has_part", slot_type=Part, key_name="PartCode", keyed=False)

        super().__post_init__(**kwargs)


@dataclass
class Part(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINCINFO.Part
    class_class_curie: ClassVar[str] = "loincinfo:Part"
    class_name: ClassVar[str] = "Part"
    class_model_uri: ClassVar[URIRef] = LOINCINFO.Part

    PartCode: str = None
    PartName: str = None
    part_type: Optional[Union[Union[dict, "PartType"], List[Union[dict, "PartType"]]]] = empty_list()
    part_of: Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]] = empty_dict()
    subclass_of: Optional[Union[dict, "Part"]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.PartCode):
            self.MissingRequiredField("PartCode")
        if not isinstance(self.PartCode, str):
            self.PartCode = str(self.PartCode)

        if self._is_empty(self.PartName):
            self.MissingRequiredField("PartName")
        if not isinstance(self.PartName, str):
            self.PartName = str(self.PartName)

        self._normalize_inlined_as_list(slot_name="part_type", slot_type=PartType, key_name="PartTypeCode", keyed=False)

        self._normalize_inlined_as_list(slot_name="part_of", slot_type=LOINC, key_name="LOINCId", keyed=True)

        if self.subclass_of is not None and not isinstance(self.subclass_of, Part):
            self.subclass_of = Part(**as_dict(self.subclass_of))

        super().__post_init__(**kwargs)


@dataclass
class PartType(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINCINFO.PartType
    class_class_curie: ClassVar[str] = "loincinfo:PartType"
    class_name: ClassVar[str] = "PartType"
    class_model_uri: ClassVar[URIRef] = LOINCINFO.PartType

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

    class_class_uri: ClassVar[URIRef] = LOINCINFO.Container
    class_class_curie: ClassVar[str] = "loincinfo:Container"
    class_name: ClassVar[str] = "Container"
    class_model_uri: ClassVar[URIRef] = LOINCINFO.Container

    LOINCData: Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="LOINCData", slot_type=LOINC, key_name="LOINCId", keyed=True)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.LOINCId = Slot(uri=LOINCINFO.LOINCId, name="LOINCId", curie=LOINCINFO.curie('LOINCId'),
                   model_uri=LOINCINFO.LOINCId, domain=None, range=URIRef)

slots.LOINCCode = Slot(uri=LOINCINFO.LOINCCode, name="LOINCCode", curie=LOINCINFO.curie('LOINCCode'),
                   model_uri=LOINCINFO.LOINCCode, domain=None, range=str)

slots.LOINCName = Slot(uri=LOINCINFO.LOINCName, name="LOINCName", curie=LOINCINFO.curie('LOINCName'),
                   model_uri=LOINCINFO.LOINCName, domain=None, range=str)

slots.has_part = Slot(uri=LOINCINFO.has_part, name="has_part", curie=LOINCINFO.curie('has_part'),
                   model_uri=LOINCINFO.has_part, domain=None, range=Optional[Union[Union[dict, Part], List[Union[dict, Part]]]])

slots.PartCode = Slot(uri=LOINCINFO.PartCode, name="PartCode", curie=LOINCINFO.curie('PartCode'),
                   model_uri=LOINCINFO.PartCode, domain=None, range=str)

slots.PartName = Slot(uri=LOINCINFO.PartName, name="PartName", curie=LOINCINFO.curie('PartName'),
                   model_uri=LOINCINFO.PartName, domain=None, range=str)

slots.part_type = Slot(uri=LOINCINFO.part_type, name="part_type", curie=LOINCINFO.curie('part_type'),
                   model_uri=LOINCINFO.part_type, domain=None, range=Optional[Union[Union[dict, PartType], List[Union[dict, PartType]]]])

slots.part_of = Slot(uri=LOINCINFO.part_of, name="part_of", curie=LOINCINFO.curie('part_of'),
                   model_uri=LOINCINFO.part_of, domain=None, range=Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]])

slots.subclass_of = Slot(uri=LOINCINFO.subclass_of, name="subclass_of", curie=LOINCINFO.curie('subclass_of'),
                   model_uri=LOINCINFO.subclass_of, domain=None, range=Optional[Union[dict, Part]])

slots.PartTypeCode = Slot(uri=LOINCINFO.PartTypeCode, name="PartTypeCode", curie=LOINCINFO.curie('PartTypeCode'),
                   model_uri=LOINCINFO.PartTypeCode, domain=None, range=str)

slots.PartTypeName = Slot(uri=LOINCINFO.PartTypeName, name="PartTypeName", curie=LOINCINFO.curie('PartTypeName'),
                   model_uri=LOINCINFO.PartTypeName, domain=None, range=str)

slots.LOINCData = Slot(uri=LOINCINFO.LOINCData, name="LOINCData", curie=LOINCINFO.curie('LOINCData'),
                   model_uri=LOINCINFO.LOINCData, domain=None, range=Optional[Union[Dict[Union[str, LOINCLOINCId], Union[dict, LOINC]], List[Union[dict, LOINC]]]])
