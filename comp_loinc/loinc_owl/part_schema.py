# Auto generated from part_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-10-07T08:40:57
# Schema: loinc-owl-part-schema
#
# id: https://loinc.org/part
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
from linkml_runtime.linkml_model.types import String, Uriorcurie
from linkml_runtime.utils.metamodelcore import URIorCURIE

metamodel_version = "1.7.0"
version = None

# Overwrite dataclasses _init_fn to add **kwargs in __init__
dataclasses._init_fn = dataclasses_init_fn_with_kwargs

# Namespaces
LINKML = CurieNamespace('linkml', 'https://w3id.org/linkml/')
LOINC = CurieNamespace('loinc', 'https://loinc.org/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
DEFAULT_ = CurieNamespace('', 'https://loinc.org/part/')


# Types

# Class references
class ThingId(URIorCURIE):
    pass


class PartClassId(ThingId):
    pass


class ComponentClassId(PartClassId):
    pass


class SystemClassId(PartClassId):
    pass


class MethodClassId(PartClassId):
    pass


class TimeClassId(PartClassId):
    pass


class PropertyClassId(PartClassId):
    pass


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/Thing")

    id: Union[str, ThingId] = None
    label: Optional[str] = None
    description: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThingId):
            self.id = ThingId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        super().__post_init__(**kwargs)


@dataclass
class PartClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/PartClass")

    id: Union[str, PartClassId] = None
    subClassOf: Union[Union[str, ThingId], List[Union[str, ThingId]]] = None
    part_number: Optional[str] = None
    part_type: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PartClassId):
            self.id = PartClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ThingId) else ThingId(v) for v in self.subClassOf]

        if self.part_number is not None and not isinstance(self.part_number, str):
            self.part_number = str(self.part_number)

        if self.part_type is not None and not isinstance(self.part_type, str):
            self.part_type = str(self.part_type)

        super().__post_init__(**kwargs)


@dataclass
class ComponentClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/ComponentClass"]
    class_class_curie: ClassVar[str] = "loinc:part/ComponentClass"
    class_name: ClassVar[str] = "ComponentClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/ComponentClass")

    id: Union[str, ComponentClassId] = None
    subClassOf: Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComponentClassId):
            self.id = ComponentClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ComponentClassId) else ComponentClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class SystemClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/SystemClass"]
    class_class_curie: ClassVar[str] = "loinc:part/SystemClass"
    class_name: ClassVar[str] = "SystemClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/SystemClass")

    id: Union[str, SystemClassId] = None
    subClassOf: Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SystemClassId):
            self.id = SystemClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, SystemClassId) else SystemClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class MethodClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/MethodClass"]
    class_class_curie: ClassVar[str] = "loinc:part/MethodClass"
    class_name: ClassVar[str] = "MethodClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/MethodClass")

    id: Union[str, MethodClassId] = None
    subClassOf: Union[Union[str, MethodClassId], List[Union[str, MethodClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MethodClassId):
            self.id = MethodClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, MethodClassId) else MethodClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class TimeClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/TimeClass"]
    class_class_curie: ClassVar[str] = "loinc:part/TimeClass"
    class_name: ClassVar[str] = "TimeClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/TimeClass")

    id: Union[str, TimeClassId] = None
    subClassOf: Union[Union[str, TimeClassId], List[Union[str, TimeClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TimeClassId):
            self.id = TimeClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, TimeClassId) else TimeClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class PropertyClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PropertyClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PropertyClass"
    class_name: ClassVar[str] = "PropertyClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/part/PropertyClass")

    id: Union[str, PropertyClassId] = None
    subClassOf: Union[Union[str, PropertyClassId], List[Union[str, PropertyClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PropertyClassId):
            self.id = PropertyClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, PropertyClassId) else PropertyClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.part_type = Slot(uri=LOINC.part_type, name="part_type", curie=LOINC.curie('part_type'),
                   model_uri=DEFAULT_.part_type, domain=None, range=Optional[str])

slots.part_number = Slot(uri=LOINC.part_number, name="part_number", curie=LOINC.curie('part_number'),
                   model_uri=DEFAULT_.part_number, domain=None, range=Optional[str])

slots.id = Slot(uri=LOINC['core/id'], name="id", curie=LOINC.curie('core/id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=DEFAULT_.label, domain=None, range=Optional[str])

slots.description = Slot(uri=RDFS.description, name="description", curie=RDFS.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=Optional[str])

slots.subClassOf = Slot(uri=RDFS.subClassOf, name="subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.subClassOf, domain=None, range=Union[Union[str, ThingId], List[Union[str, ThingId]]])

slots.ComponentClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ComponentClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.ComponentClass_subClassOf, domain=ComponentClass, range=Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]])

slots.SystemClass_subClassOf = Slot(uri=RDFS.subClassOf, name="SystemClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.SystemClass_subClassOf, domain=SystemClass, range=Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]])

slots.MethodClass_subClassOf = Slot(uri=RDFS.subClassOf, name="MethodClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.MethodClass_subClassOf, domain=MethodClass, range=Union[Union[str, MethodClassId], List[Union[str, MethodClassId]]])

slots.TimeClass_subClassOf = Slot(uri=RDFS.subClassOf, name="TimeClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.TimeClass_subClassOf, domain=TimeClass, range=Union[Union[str, TimeClassId], List[Union[str, TimeClassId]]])

slots.PropertyClass_subClassOf = Slot(uri=RDFS.subClassOf, name="PropertyClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.PropertyClass_subClassOf, domain=PropertyClass, range=Union[Union[str, PropertyClassId], List[Union[str, PropertyClassId]]])
