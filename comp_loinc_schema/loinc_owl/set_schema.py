# Auto generated from set_schema.yaml by pythongen.py version: 0.9.0
# Generation date: 2022-03-25T15:02:49
# Schema: loinc-owl-set-schema
#
# id: https://loinc.org/set
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
DEFAULT_ = CurieNamespace('', 'https://loinc.org/set/')


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


@dataclass
class LoincCodeOntology(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["set/LoincCodeOntology"]
    class_class_curie: ClassVar[str] = "loinc:set/LoincCodeOntology"
    class_name: ClassVar[str] = "LoincCodeOntology"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/LoincCodeOntology")

    component_class_set: Optional[Union[Dict[Union[str, ComponentClassId], Union[dict, "ComponentClass"]], List[Union[dict, "ComponentClass"]]]] = empty_dict()
    system_class_set: Optional[Union[Dict[Union[str, SystemClassId], Union[dict, "SystemClass"]], List[Union[dict, "SystemClass"]]]] = empty_dict()
    code_class_set: Optional[Union[Dict[Union[str, LoincCodeClassId], Union[dict, "LoincCodeClass"]], List[Union[dict, "LoincCodeClass"]]]] = empty_dict()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        self._normalize_inlined_as_list(slot_name="component_class_set", slot_type=ComponentClass, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="system_class_set", slot_type=SystemClass, key_name="id", keyed=True)

        self._normalize_inlined_as_list(slot_name="code_class_set", slot_type=LoincCodeClass, key_name="id", keyed=True)

        super().__post_init__(**kwargs)


@dataclass
class Thing(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/Thing")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/LoincCodeClass")

    id: Union[str, LoincCodeClassId] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincCodeClassId):
            self.id = LoincCodeClassId(self.id)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        super().__post_init__(**kwargs)


@dataclass
class PartClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/PartClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/ComponentClass")

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
    class_model_uri: ClassVar[URIRef] = URIRef("https://loinc.org/set/SystemClass")

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


# Enumerations


# Slots
class slots:
    pass

slots.component_class_set = Slot(uri=DEFAULT_.component_class_set, name="component_class_set", curie=DEFAULT_.curie('component_class_set'),
                   model_uri=DEFAULT_.component_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, ComponentClassId], Union[dict, "ComponentClass"]], List[Union[dict, "ComponentClass"]]]])

slots.system_class_set = Slot(uri=DEFAULT_.system_class_set, name="system_class_set", curie=DEFAULT_.curie('system_class_set'),
                   model_uri=DEFAULT_.system_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, SystemClassId], Union[dict, "SystemClass"]], List[Union[dict, "SystemClass"]]]])

slots.code_class_set = Slot(uri=DEFAULT_.code_class_set, name="code_class_set", curie=DEFAULT_.curie('code_class_set'),
                   model_uri=DEFAULT_.code_class_set, domain=LoincCodeOntology, range=Optional[Union[Dict[Union[str, LoincCodeClassId], Union[dict, "LoincCodeClass"]], List[Union[dict, "LoincCodeClass"]]]])

slots.id = Slot(uri=LOINC['core/id'], name="id", curie=LOINC.curie('core/id'),
                   model_uri=DEFAULT_.id, domain=None, range=URIRef)

slots.label = Slot(uri=RDFS.label, name="label", curie=RDFS.curie('label'),
                   model_uri=DEFAULT_.label, domain=None, range=Optional[str])

slots.description = Slot(uri=RDFS.description, name="description", curie=RDFS.curie('description'),
                   model_uri=DEFAULT_.description, domain=None, range=Optional[str])

slots.subClassOf = Slot(uri=RDFS.subClassOf, name="subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.subClassOf, domain=None, range=Union[Union[str, PartClassId], List[Union[str, PartClassId]]])

slots.loincCodeClass__has_component = Slot(uri=DEFAULT_.has_component, name="loincCodeClass__has_component", curie=DEFAULT_.curie('has_component'),
                   model_uri=DEFAULT_.loincCodeClass__has_component, domain=None, range=Optional[Union[str, ComponentClassId]])

slots.loincCodeClass__has_system = Slot(uri=DEFAULT_.has_system, name="loincCodeClass__has_system", curie=DEFAULT_.curie('has_system'),
                   model_uri=DEFAULT_.loincCodeClass__has_system, domain=None, range=Optional[Union[str, SystemClassId]])

slots.ComponentClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ComponentClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.ComponentClass_subClassOf, domain=ComponentClass, range=Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]])

slots.SystemClass_subClassOf = Slot(uri=RDFS.subClassOf, name="SystemClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=DEFAULT_.SystemClass_subClassOf, domain=SystemClass, range=Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]])
