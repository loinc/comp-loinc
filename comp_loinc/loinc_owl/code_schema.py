# Auto generated from code_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-06-29T09:10:26
# Schema: loinc-owl-code-schema
#
# id: https://loinc.org/code
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
DEFAULT_ = CurieNamespace('', 'https://loinc.org/code/')


# Types

# Class references
class ThingId(URIorCURIE):
    pass


class LoincCodeClassId(ThingId):
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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/Thing")

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
class LoincCodeClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClass"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClass"
    class_name: ClassVar[str] = "LoincCodeClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/LoincCodeClass")

    id: Union[str, LoincCodeClassId] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None
    has_method: Optional[Union[str, MethodClassId]] = None
    has_property: Optional[Union[str, PropertyClassId]] = None
    has_time: Optional[Union[str, TimeClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincCodeClassId):
            self.id = LoincCodeClassId(self.id)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        if self.has_method is not None and not isinstance(self.has_method, MethodClassId):
            self.has_method = MethodClassId(self.has_method)

        if self.has_property is not None and not isinstance(self.has_property, PropertyClassId):
            self.has_property = PropertyClassId(self.has_property)

        if self.has_time is not None and not isinstance(self.has_time, TimeClassId):
            self.has_time = TimeClassId(self.has_time)

        super().__post_init__(**kwargs)


@dataclass
class PartClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/PartClass")

    id: Union[str, PartClassId] = None
    subClassOf: Union[Union[str, PartClassId], List[Union[str, PartClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PartClassId):
            self.id = PartClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, PartClassId) else PartClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class ComponentClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/ComponentClass"]
    class_class_curie: ClassVar[str] = "loinc:part/ComponentClass"
    class_name: ClassVar[str] = "ComponentClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/ComponentClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/SystemClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/MethodClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/TimeClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/code/PropertyClass")

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

slots.has_component = Slot(uri=LOINC.hasComponent, name="has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=DEFAULT_.has_component, domain=None, range=Optional[Union[str, ComponentClassId]])

slots.has_system = Slot(uri=LOINC.hasSystem, name="has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=DEFAULT_.has_system, domain=None, range=Optional[Union[str, SystemClassId]])

slots.has_method = Slot(uri=LOINC.hasMethod, name="has_method", curie=LOINC.curie('hasMethod'),
                   model_uri=DEFAULT_.has_method, domain=None, range=Optional[Union[str, MethodClassId]])

slots.has_property = Slot(uri=LOINC.hasProperty, name="has_property", curie=LOINC.curie('hasProperty'),
                   model_uri=DEFAULT_.has_property, domain=None, range=Optional[Union[str, PropertyClassId]])

slots.has_time = Slot(uri=LOINC.hasTime, name="has_time", curie=LOINC.curie('hasTime'),
                   model_uri=DEFAULT_.has_time, domain=None, range=Optional[Union[str, TimeClassId]])

slots.id = Slot(uri=LOINC['core/id'], name="id", curie=LOINC.curie('core/id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=DEFAULT_.label, domain=None, range=Optional[str])

slots.description = Slot(uri=RDFS.description, name="description", curie=RDFS.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=Optional[str])

slots.subClassOf = Slot(uri=RDFS.subClassOf, name="subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.subClassOf, domain=None, range=Union[Union[str, PartClassId], List[Union[str, PartClassId]]])

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
