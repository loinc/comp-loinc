# Auto generated from comp_loinc.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-03-29T11:41:06
# Schema: loinc-owl-core-schema
#
# id: https://loinc.org/core
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
DEFAULT_ = LOINC


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


class ScaleClassId(PartClassId):
    pass


class CodeBySystemId(ThingId):
    pass


class CodeByComponentId(ThingId):
    pass


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = LOINC.Thing

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
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClass

    id: Union[str, LoincCodeClassId] = None
    subClassOf: Union[Union[str, LoincCodeClassId], List[Union[str, LoincCodeClassId]]] = None
    formal_name: Optional[str] = None
    loinc_number: Optional[str] = None
    status: Optional[str] = None
    short_name: Optional[str] = None
    long_common_name: Optional[str] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_property: Optional[Union[str, PropertyClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None
    has_method: Optional[Union[str, MethodClassId]] = None
    has_scale: Optional[Union[str, ScaleClassId]] = None
    has_time: Optional[Union[str, TimeClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincCodeClassId):
            self.id = LoincCodeClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, LoincCodeClassId) else LoincCodeClassId(v) for v in self.subClassOf]

        if self.formal_name is not None and not isinstance(self.formal_name, str):
            self.formal_name = str(self.formal_name)

        if self.loinc_number is not None and not isinstance(self.loinc_number, str):
            self.loinc_number = str(self.loinc_number)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.long_common_name is not None and not isinstance(self.long_common_name, str):
            self.long_common_name = str(self.long_common_name)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_property is not None and not isinstance(self.has_property, PropertyClassId):
            self.has_property = PropertyClassId(self.has_property)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        if self.has_method is not None and not isinstance(self.has_method, MethodClassId):
            self.has_method = MethodClassId(self.has_method)

        if self.has_scale is not None and not isinstance(self.has_scale, ScaleClassId):
            self.has_scale = ScaleClassId(self.has_scale)

        if self.has_time is not None and not isinstance(self.has_time, TimeClassId):
            self.has_time = TimeClassId(self.has_time)

        super().__post_init__(**kwargs)


@dataclass
class PartClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = LOINC.PartClass

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
    class_model_uri: ClassVar[URIRef] = LOINC.ComponentClass

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
    class_model_uri: ClassVar[URIRef] = LOINC.SystemClass

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
    class_model_uri: ClassVar[URIRef] = LOINC.MethodClass

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
    class_model_uri: ClassVar[URIRef] = LOINC.TimeClass

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
    class_model_uri: ClassVar[URIRef] = LOINC.PropertyClass

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


@dataclass
class ScaleClass(PartClass):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/ScaleClass"]
    class_class_curie: ClassVar[str] = "loinc:part/ScaleClass"
    class_name: ClassVar[str] = "ScaleClass"
    class_model_uri: ClassVar[URIRef] = LOINC.ScaleClass

    id: Union[str, ScaleClassId] = None
    subClassOf: Union[Union[str, ScaleClassId], List[Union[str, ScaleClassId]]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScaleClassId):
            self.id = ScaleClassId(self.id)

        if self._is_empty(self.subClassOf):
            self.MissingRequiredField("subClassOf")
        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ScaleClassId) else ScaleClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class LoincCodeOntology(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["set/LoincCodeOntology"]
    class_class_curie: ClassVar[str] = "loinc:set/LoincCodeOntology"
    class_name: ClassVar[str] = "LoincCodeOntology"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeOntology

    component_class_set: Optional[Union[Dict[Union[str, ComponentClassId], Union[dict, ComponentClass]], List[Union[dict, ComponentClass]]]] = empty_dict()
    system_class_set: Optional[Union[Dict[Union[str, SystemClassId], Union[dict, SystemClass]], List[Union[dict, SystemClass]]]] = empty_dict()
    code_class_set: Optional[Union[Dict[Union[str, LoincCodeClassId], Union[dict, LoincCodeClass]], List[Union[dict, LoincCodeClass]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="component_class_set", slot_type=ComponentClass, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="system_class_set", slot_type=SystemClass, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="code_class_set", slot_type=LoincCodeClass, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class CodeBySystem(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["grouping_classes/CodeBySystem"]
    class_class_curie: ClassVar[str] = "loinc:grouping_classes/CodeBySystem"
    class_name: ClassVar[str] = "CodeBySystem"
    class_model_uri: ClassVar[URIRef] = LOINC.CodeBySystem

    id: Union[str, CodeBySystemId] = None
    has_system: Optional[Union[str, SystemClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CodeBySystemId):
            self.id = CodeBySystemId(self.id)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        super().__post_init__(**kwargs)


@dataclass
class CodeByComponent(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["grouping_classes/CodeByComponent"]
    class_class_curie: ClassVar[str] = "loinc:grouping_classes/CodeByComponent"
    class_name: ClassVar[str] = "CodeByComponent"
    class_model_uri: ClassVar[URIRef] = LOINC.CodeByComponent

    id: Union[str, CodeByComponentId] = None
    has_component: Optional[Union[str, ComponentClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, CodeByComponentId):
            self.id = CodeByComponentId(self.id)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.id = Slot(uri=LOINC.id, name="id", curie=LOINC.curie('id'),
                   model_uri=LOINC.id, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=LOINC.label, domain=None, range=Optional[str])

slots.description = Slot(uri=RDFS.description, name="description", curie=RDFS.curie('description'),
                   model_uri=LOINC.description, domain=None, range=Optional[str])

slots.subClassOf = Slot(uri=RDFS.subClassOf, name="subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.subClassOf, domain=None, range=Union[Union[str, ThingId], List[Union[str, ThingId]]])

slots.formal_name = Slot(uri=LOINC.formal_name, name="formal_name", curie=LOINC.curie('formal_name'),
                   model_uri=LOINC.formal_name, domain=None, range=Optional[str])

slots.loinc_number = Slot(uri=LOINC.loinc_number, name="loinc_number", curie=LOINC.curie('loinc_number'),
                   model_uri=LOINC.loinc_number, domain=None, range=Optional[str])

slots.status = Slot(uri=LOINC.status, name="status", curie=LOINC.curie('status'),
                   model_uri=LOINC.status, domain=None, range=Optional[str])

slots.long_common_name = Slot(uri=LOINC.long_common_name, name="long_common_name", curie=LOINC.curie('long_common_name'),
                   model_uri=LOINC.long_common_name, domain=None, range=Optional[str])

slots.short_name = Slot(uri=LOINC.short_name, name="short_name", curie=LOINC.curie('short_name'),
                   model_uri=LOINC.short_name, domain=None, range=Optional[str])

slots.has_component = Slot(uri=LOINC.hasComponent, name="has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=LOINC.has_component, domain=None, range=Optional[Union[str, ComponentClassId]])

slots.has_system = Slot(uri=LOINC.hasSystem, name="has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=LOINC.has_system, domain=None, range=Optional[Union[str, SystemClassId]])

slots.has_method = Slot(uri=LOINC.hasMethod, name="has_method", curie=LOINC.curie('hasMethod'),
                   model_uri=LOINC.has_method, domain=None, range=Optional[Union[str, MethodClassId]])

slots.has_property = Slot(uri=LOINC.hasProperty, name="has_property", curie=LOINC.curie('hasProperty'),
                   model_uri=LOINC.has_property, domain=None, range=Optional[Union[str, PropertyClassId]])

slots.has_time = Slot(uri=LOINC.hasTime, name="has_time", curie=LOINC.curie('hasTime'),
                   model_uri=LOINC.has_time, domain=None, range=Optional[Union[str, TimeClassId]])

slots.has_scale = Slot(uri=LOINC.hasScale, name="has_scale", curie=LOINC.curie('hasScale'),
                   model_uri=LOINC.has_scale, domain=None, range=Optional[Union[str, ScaleClassId]])

slots.part_type = Slot(uri=LOINC.part_type, name="part_type", curie=LOINC.curie('part_type'),
                   model_uri=LOINC.part_type, domain=None, range=Optional[str])

slots.part_number = Slot(uri=LOINC.part_number, name="part_number", curie=LOINC.curie('part_number'),
                   model_uri=LOINC.part_number, domain=None, range=Optional[str])

slots.component_class_set = Slot(uri=LOINC['set/component_class_set'], name="component_class_set", curie=LOINC.curie('set/component_class_set'),
                   model_uri=LOINC.component_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, ComponentClassId], Union[dict, ComponentClass]], List[Union[dict, ComponentClass]]]])

slots.system_class_set = Slot(uri=LOINC['set/system_class_set'], name="system_class_set", curie=LOINC.curie('set/system_class_set'),
                   model_uri=LOINC.system_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, SystemClassId], Union[dict, SystemClass]], List[Union[dict, SystemClass]]]])

slots.code_class_set = Slot(uri=LOINC['set/code_class_set'], name="code_class_set", curie=LOINC.curie('set/code_class_set'),
                   model_uri=LOINC.code_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, LoincCodeClassId], Union[dict, LoincCodeClass]], List[Union[dict, LoincCodeClass]]]])

slots.LoincCodeClass_subClassOf = Slot(uri=RDFS.subClassOf, name="LoincCodeClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.LoincCodeClass_subClassOf, domain=LoincCodeClass, range=Union[Union[str, LoincCodeClassId], List[Union[str, LoincCodeClassId]]])

slots.ComponentClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ComponentClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.ComponentClass_subClassOf, domain=ComponentClass, range=Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]])

slots.SystemClass_subClassOf = Slot(uri=RDFS.subClassOf, name="SystemClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.SystemClass_subClassOf, domain=SystemClass, range=Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]])

slots.MethodClass_subClassOf = Slot(uri=RDFS.subClassOf, name="MethodClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.MethodClass_subClassOf, domain=MethodClass, range=Union[Union[str, MethodClassId], List[Union[str, MethodClassId]]])

slots.TimeClass_subClassOf = Slot(uri=RDFS.subClassOf, name="TimeClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.TimeClass_subClassOf, domain=TimeClass, range=Union[Union[str, TimeClassId], List[Union[str, TimeClassId]]])

slots.PropertyClass_subClassOf = Slot(uri=RDFS.subClassOf, name="PropertyClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.PropertyClass_subClassOf, domain=PropertyClass, range=Union[Union[str, PropertyClassId], List[Union[str, PropertyClassId]]])

slots.ScaleClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ScaleClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.ScaleClass_subClassOf, domain=ScaleClass, range=Union[Union[str, ScaleClassId], List[Union[str, ScaleClassId]]])

slots.CodeBySystem_has_system = Slot(uri=LOINC.hasSystem, name="CodeBySystem_has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=LOINC.CodeBySystem_has_system, domain=CodeBySystem, range=Optional[Union[str, SystemClassId]])

slots.CodeByComponent_has_component = Slot(uri=LOINC.hasComponent, name="CodeByComponent_has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=LOINC.CodeByComponent_has_component, domain=CodeByComponent, range=Optional[Union[str, ComponentClassId]])