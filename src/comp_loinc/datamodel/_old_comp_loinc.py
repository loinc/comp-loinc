# Auto generated from comp_loinc.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-11-09T11:51:11
# Schema: loinc-owl-core-schema
#
# id: https://loinc.org/core
# description:
# license: https://creativecommons.org/publicdomain/zero/1.0/

import dataclasses
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
class LoincEntityId(URIorCURIE):
    pass


class LoincTermId(LoincEntityId):
    pass


class LoincTermIntersectionId(LoincTermId):
    pass


class LoincTermNonIntersectionId(LoincTermId):
    pass


class PartClassId(LoincEntityId):
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


@dataclass
class LoincEntity(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Thing"
    class_model_uri: ClassVar[URIRef] = LOINC.Thing

    id: Union[str, LoincEntityId] = None
    label: Optional[str] = None
    description: Optional[str] = None
    subClassOf: Optional[Union[Union[str, LoincEntityId], List[Union[str, LoincEntityId]]]] = empty_list()
    equivalentClasses: Optional[Union[Union[str, LoincEntityId], List[Union[str, LoincEntityId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincEntityId):
            self.id = LoincEntityId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, LoincEntityId) else LoincEntityId(v) for v in self.subClassOf]

        if not isinstance(self.equivalentClasses, list):
            self.equivalentClasses = [self.equivalentClasses] if self.equivalentClasses is not None else []
        self.equivalentClasses = [v if isinstance(v, LoincEntityId) else LoincEntityId(v) for v in self.equivalentClasses]

        super().__post_init__(**kwargs)


@dataclass
class Loinc(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL.Class
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Loinc"
    class_model_uri: ClassVar[URIRef] = LOINC.Loinc

    codes: Optional[Union[Union[str, LoincTermId], List[Union[str, LoincTermId]]]] = empty_list()
    parts: Optional[Union[Union[str, PartClassId], List[Union[str, PartClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.codes, list):
            self.codes = [self.codes] if self.codes is not None else []
        self.codes = [v if isinstance(v, LoincTermId) else LoincTermId(v) for v in self.codes]

        if not isinstance(self.parts, list):
            self.parts = [self.parts] if self.parts is not None else []
        self.parts = [v if isinstance(v, PartClassId) else PartClassId(v) for v in self.parts]

        super().__post_init__(**kwargs)


@dataclass
class LoincTerm(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClass"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClass"
    class_name: ClassVar[str] = "LoincCodeClass"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClass

    id: Union[str, LoincTermId] = None
    loinc_number: Optional[str] = None
    long_common_name: Optional[str] = None
    formal_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
    loinc_class: Optional[str] = None
    loinc_class_type: Optional[str] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_property: Optional[Union[str, PropertyClassId]] = None
    has_time: Optional[Union[str, TimeClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None
    has_scale: Optional[Union[str, ScaleClassId]] = None
    has_method: Optional[Union[str, MethodClassId]] = None
    has_component_analyte: Optional[Union[str, PartClassId]] = None
    has_component_challenge: Optional[Union[str, PartClassId]] = None
    has_component_count: Optional[Union[str, PartClassId]] = None
    has_component_adjustment: Optional[Union[str, PartClassId]] = None
    has_time_core: Optional[Union[str, PartClassId]] = None
    has_time_modifier: Optional[Union[str, PartClassId]] = None
    has_system_core: Optional[Union[str, PartClassId]] = None
    has_system_super_system: Optional[Union[str, PartClassId]] = None
    semantic_analyte_gene: Optional[Union[str, PartClassId]] = None
    syntax_analyte_core: Optional[Union[str, PartClassId]] = None
    syntax_analyte_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_numerator: Optional[Union[str, PartClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincTermId):
            self.id = LoincTermId(self.id)

        if self.loinc_number is not None and not isinstance(self.loinc_number, str):
            self.loinc_number = str(self.loinc_number)

        if self.long_common_name is not None and not isinstance(self.long_common_name, str):
            self.long_common_name = str(self.long_common_name)

        if self.formal_name is not None and not isinstance(self.formal_name, str):
            self.formal_name = str(self.formal_name)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.loinc_class is not None and not isinstance(self.loinc_class, str):
            self.loinc_class = str(self.loinc_class)

        if self.loinc_class_type is not None and not isinstance(self.loinc_class_type, str):
            self.loinc_class_type = str(self.loinc_class_type)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_property is not None and not isinstance(self.has_property, PropertyClassId):
            self.has_property = PropertyClassId(self.has_property)

        if self.has_time is not None and not isinstance(self.has_time, TimeClassId):
            self.has_time = TimeClassId(self.has_time)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        if self.has_scale is not None and not isinstance(self.has_scale, ScaleClassId):
            self.has_scale = ScaleClassId(self.has_scale)

        if self.has_method is not None and not isinstance(self.has_method, MethodClassId):
            self.has_method = MethodClassId(self.has_method)

        if self.has_component_analyte is not None and not isinstance(self.has_component_analyte, PartClassId):
            self.has_component_analyte = PartClassId(self.has_component_analyte)

        if self.has_component_challenge is not None and not isinstance(self.has_component_challenge, PartClassId):
            self.has_component_challenge = PartClassId(self.has_component_challenge)

        if self.has_component_count is not None and not isinstance(self.has_component_count, PartClassId):
            self.has_component_count = PartClassId(self.has_component_count)

        if self.has_component_adjustment is not None and not isinstance(self.has_component_adjustment, PartClassId):
            self.has_component_adjustment = PartClassId(self.has_component_adjustment)

        if self.has_time_core is not None and not isinstance(self.has_time_core, PartClassId):
            self.has_time_core = PartClassId(self.has_time_core)

        if self.has_time_modifier is not None and not isinstance(self.has_time_modifier, PartClassId):
            self.has_time_modifier = PartClassId(self.has_time_modifier)

        if self.has_system_core is not None and not isinstance(self.has_system_core, PartClassId):
            self.has_system_core = PartClassId(self.has_system_core)

        if self.has_system_super_system is not None and not isinstance(self.has_system_super_system, PartClassId):
            self.has_system_super_system = PartClassId(self.has_system_super_system)

        if self.semantic_analyte_gene is not None and not isinstance(self.semantic_analyte_gene, PartClassId):
            self.semantic_analyte_gene = PartClassId(self.semantic_analyte_gene)

        if self.syntax_analyte_core is not None and not isinstance(self.syntax_analyte_core, PartClassId):
            self.syntax_analyte_core = PartClassId(self.syntax_analyte_core)

        if self.syntax_analyte_suffix is not None and not isinstance(self.syntax_analyte_suffix, PartClassId):
            self.syntax_analyte_suffix = PartClassId(self.syntax_analyte_suffix)

        if self.syntax_analyte_divisor is not None and not isinstance(self.syntax_analyte_divisor, PartClassId):
            self.syntax_analyte_divisor = PartClassId(self.syntax_analyte_divisor)

        if self.syntax_analyte_divisor_suffix is not None and not isinstance(self.syntax_analyte_divisor_suffix, PartClassId):
            self.syntax_analyte_divisor_suffix = PartClassId(self.syntax_analyte_divisor_suffix)

        if self.syntax_analyte_numerator is not None and not isinstance(self.syntax_analyte_numerator, PartClassId):
            self.syntax_analyte_numerator = PartClassId(self.syntax_analyte_numerator)

        super().__post_init__(**kwargs)


@dataclass
class LoincTermIntersection(LoincTerm):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClassIntersection"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClassIntersection"
    class_name: ClassVar[str] = "LoincCodeClassIntersection"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClassIntersection

    id: Union[str, LoincTermIntersectionId] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_property: Optional[Union[str, PropertyClassId]] = None
    has_time: Optional[Union[str, TimeClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None
    has_scale: Optional[Union[str, ScaleClassId]] = None
    has_method: Optional[Union[str, MethodClassId]] = None
    has_component_analyte: Optional[Union[str, PartClassId]] = None
    has_component_challenge: Optional[Union[str, PartClassId]] = None
    has_component_count: Optional[Union[str, PartClassId]] = None
    has_component_adjustment: Optional[Union[str, PartClassId]] = None
    has_time_core: Optional[Union[str, PartClassId]] = None
    has_time_modifier: Optional[Union[str, PartClassId]] = None
    has_system_core: Optional[Union[str, PartClassId]] = None
    has_system_super_system: Optional[Union[str, PartClassId]] = None
    semantic_analyte_gene: Optional[Union[str, PartClassId]] = None
    syntax_analyte_core: Optional[Union[str, PartClassId]] = None
    syntax_analyte_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_numerator: Optional[Union[str, PartClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincTermIntersectionId):
            self.id = LoincTermIntersectionId(self.id)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_property is not None and not isinstance(self.has_property, PropertyClassId):
            self.has_property = PropertyClassId(self.has_property)

        if self.has_time is not None and not isinstance(self.has_time, TimeClassId):
            self.has_time = TimeClassId(self.has_time)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        if self.has_scale is not None and not isinstance(self.has_scale, ScaleClassId):
            self.has_scale = ScaleClassId(self.has_scale)

        if self.has_method is not None and not isinstance(self.has_method, MethodClassId):
            self.has_method = MethodClassId(self.has_method)

        if self.has_component_analyte is not None and not isinstance(self.has_component_analyte, PartClassId):
            self.has_component_analyte = PartClassId(self.has_component_analyte)

        if self.has_component_challenge is not None and not isinstance(self.has_component_challenge, PartClassId):
            self.has_component_challenge = PartClassId(self.has_component_challenge)

        if self.has_component_count is not None and not isinstance(self.has_component_count, PartClassId):
            self.has_component_count = PartClassId(self.has_component_count)

        if self.has_component_adjustment is not None and not isinstance(self.has_component_adjustment, PartClassId):
            self.has_component_adjustment = PartClassId(self.has_component_adjustment)

        if self.has_time_core is not None and not isinstance(self.has_time_core, PartClassId):
            self.has_time_core = PartClassId(self.has_time_core)

        if self.has_time_modifier is not None and not isinstance(self.has_time_modifier, PartClassId):
            self.has_time_modifier = PartClassId(self.has_time_modifier)

        if self.has_system_core is not None and not isinstance(self.has_system_core, PartClassId):
            self.has_system_core = PartClassId(self.has_system_core)

        if self.has_system_super_system is not None and not isinstance(self.has_system_super_system, PartClassId):
            self.has_system_super_system = PartClassId(self.has_system_super_system)

        if self.semantic_analyte_gene is not None and not isinstance(self.semantic_analyte_gene, PartClassId):
            self.semantic_analyte_gene = PartClassId(self.semantic_analyte_gene)

        if self.syntax_analyte_core is not None and not isinstance(self.syntax_analyte_core, PartClassId):
            self.syntax_analyte_core = PartClassId(self.syntax_analyte_core)

        if self.syntax_analyte_suffix is not None and not isinstance(self.syntax_analyte_suffix, PartClassId):
            self.syntax_analyte_suffix = PartClassId(self.syntax_analyte_suffix)

        if self.syntax_analyte_divisor is not None and not isinstance(self.syntax_analyte_divisor, PartClassId):
            self.syntax_analyte_divisor = PartClassId(self.syntax_analyte_divisor)

        if self.syntax_analyte_divisor_suffix is not None and not isinstance(self.syntax_analyte_divisor_suffix, PartClassId):
            self.syntax_analyte_divisor_suffix = PartClassId(self.syntax_analyte_divisor_suffix)

        if self.syntax_analyte_numerator is not None and not isinstance(self.syntax_analyte_numerator, PartClassId):
            self.syntax_analyte_numerator = PartClassId(self.syntax_analyte_numerator)

        super().__post_init__(**kwargs)


@dataclass
class LoincTermNonIntersection(LoincTerm):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClassNonIntersection"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClassNonIntersection"
    class_name: ClassVar[str] = "LoincCodeClassNonIntersection"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClassNonIntersection

    id: Union[str, LoincTermNonIntersectionId] = None
    has_component: Optional[Union[str, ComponentClassId]] = None
    has_property: Optional[Union[str, PropertyClassId]] = None
    has_time: Optional[Union[str, TimeClassId]] = None
    has_system: Optional[Union[str, SystemClassId]] = None
    has_scale: Optional[Union[str, ScaleClassId]] = None
    has_method: Optional[Union[str, MethodClassId]] = None
    has_component_analyte: Optional[Union[str, PartClassId]] = None
    has_component_challenge: Optional[Union[str, PartClassId]] = None
    has_component_count: Optional[Union[str, PartClassId]] = None
    has_component_adjustment: Optional[Union[str, PartClassId]] = None
    has_time_core: Optional[Union[str, PartClassId]] = None
    has_time_modifier: Optional[Union[str, PartClassId]] = None
    has_system_core: Optional[Union[str, PartClassId]] = None
    has_system_super_system: Optional[Union[str, PartClassId]] = None
    semantic_analyte_gene: Optional[Union[str, PartClassId]] = None
    syntax_analyte_core: Optional[Union[str, PartClassId]] = None
    syntax_analyte_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor: Optional[Union[str, PartClassId]] = None
    syntax_analyte_divisor_suffix: Optional[Union[str, PartClassId]] = None
    syntax_analyte_numerator: Optional[Union[str, PartClassId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincTermNonIntersectionId):
            self.id = LoincTermNonIntersectionId(self.id)

        if self.has_component is not None and not isinstance(self.has_component, ComponentClassId):
            self.has_component = ComponentClassId(self.has_component)

        if self.has_property is not None and not isinstance(self.has_property, PropertyClassId):
            self.has_property = PropertyClassId(self.has_property)

        if self.has_time is not None and not isinstance(self.has_time, TimeClassId):
            self.has_time = TimeClassId(self.has_time)

        if self.has_system is not None and not isinstance(self.has_system, SystemClassId):
            self.has_system = SystemClassId(self.has_system)

        if self.has_scale is not None and not isinstance(self.has_scale, ScaleClassId):
            self.has_scale = ScaleClassId(self.has_scale)

        if self.has_method is not None and not isinstance(self.has_method, MethodClassId):
            self.has_method = MethodClassId(self.has_method)

        if self.has_component_analyte is not None and not isinstance(self.has_component_analyte, PartClassId):
            self.has_component_analyte = PartClassId(self.has_component_analyte)

        if self.has_component_challenge is not None and not isinstance(self.has_component_challenge, PartClassId):
            self.has_component_challenge = PartClassId(self.has_component_challenge)

        if self.has_component_count is not None and not isinstance(self.has_component_count, PartClassId):
            self.has_component_count = PartClassId(self.has_component_count)

        if self.has_component_adjustment is not None and not isinstance(self.has_component_adjustment, PartClassId):
            self.has_component_adjustment = PartClassId(self.has_component_adjustment)

        if self.has_time_core is not None and not isinstance(self.has_time_core, PartClassId):
            self.has_time_core = PartClassId(self.has_time_core)

        if self.has_time_modifier is not None and not isinstance(self.has_time_modifier, PartClassId):
            self.has_time_modifier = PartClassId(self.has_time_modifier)

        if self.has_system_core is not None and not isinstance(self.has_system_core, PartClassId):
            self.has_system_core = PartClassId(self.has_system_core)

        if self.has_system_super_system is not None and not isinstance(self.has_system_super_system, PartClassId):
            self.has_system_super_system = PartClassId(self.has_system_super_system)

        if self.semantic_analyte_gene is not None and not isinstance(self.semantic_analyte_gene, PartClassId):
            self.semantic_analyte_gene = PartClassId(self.semantic_analyte_gene)

        if self.syntax_analyte_core is not None and not isinstance(self.syntax_analyte_core, PartClassId):
            self.syntax_analyte_core = PartClassId(self.syntax_analyte_core)

        if self.syntax_analyte_suffix is not None and not isinstance(self.syntax_analyte_suffix, PartClassId):
            self.syntax_analyte_suffix = PartClassId(self.syntax_analyte_suffix)

        if self.syntax_analyte_divisor is not None and not isinstance(self.syntax_analyte_divisor, PartClassId):
            self.syntax_analyte_divisor = PartClassId(self.syntax_analyte_divisor)

        if self.syntax_analyte_divisor_suffix is not None and not isinstance(self.syntax_analyte_divisor_suffix, PartClassId):
            self.syntax_analyte_divisor_suffix = PartClassId(self.syntax_analyte_divisor_suffix)

        if self.syntax_analyte_numerator is not None and not isinstance(self.syntax_analyte_numerator, PartClassId):
            self.syntax_analyte_numerator = PartClassId(self.syntax_analyte_numerator)

        super().__post_init__(**kwargs)


@dataclass
class LoincPart(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = LOINC.PartClass

    id: Union[str, PartClassId] = None
    subClassOf: Optional[Union[Union[str, LoincEntityId], List[Union[str, LoincEntityId]]]] = empty_list()
    part_number: Optional[str] = None
    part_type: Optional[str] = None
    part_name: Optional[str] = None
    part_display_name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PartClassId):
            self.id = PartClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, LoincEntityId) else LoincEntityId(v) for v in self.subClassOf]

        if self.part_number is not None and not isinstance(self.part_number, str):
            self.part_number = str(self.part_number)

        if self.part_type is not None and not isinstance(self.part_type, str):
            self.part_type = str(self.part_type)

        if self.part_name is not None and not isinstance(self.part_name, str):
            self.part_name = str(self.part_name)

        if self.part_display_name is not None and not isinstance(self.part_display_name, str):
            self.part_display_name = str(self.part_display_name)

        super().__post_init__(**kwargs)


@dataclass
class ComponentClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/ComponentClass"]
    class_class_curie: ClassVar[str] = "loinc:part/ComponentClass"
    class_name: ClassVar[str] = "ComponentClass"
    class_model_uri: ClassVar[URIRef] = LOINC.ComponentClass

    id: Union[str, ComponentClassId] = None
    subClassOf: Optional[Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ComponentClassId):
            self.id = ComponentClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ComponentClassId) else ComponentClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class SystemClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/SystemClass"]
    class_class_curie: ClassVar[str] = "loinc:part/SystemClass"
    class_name: ClassVar[str] = "SystemClass"
    class_model_uri: ClassVar[URIRef] = LOINC.SystemClass

    id: Union[str, SystemClassId] = None
    subClassOf: Optional[Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SystemClassId):
            self.id = SystemClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, SystemClassId) else SystemClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class MethodClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/MethodClass"]
    class_class_curie: ClassVar[str] = "loinc:part/MethodClass"
    class_name: ClassVar[str] = "MethodClass"
    class_model_uri: ClassVar[URIRef] = LOINC.MethodClass

    id: Union[str, MethodClassId] = None
    subClassOf: Optional[Union[Union[str, MethodClassId], List[Union[str, MethodClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, MethodClassId):
            self.id = MethodClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, MethodClassId) else MethodClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class TimeClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/TimeClass"]
    class_class_curie: ClassVar[str] = "loinc:part/TimeClass"
    class_name: ClassVar[str] = "TimeClass"
    class_model_uri: ClassVar[URIRef] = LOINC.TimeClass

    id: Union[str, TimeClassId] = None
    subClassOf: Optional[Union[Union[str, TimeClassId], List[Union[str, TimeClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, TimeClassId):
            self.id = TimeClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, TimeClassId) else TimeClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class PropertyClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PropertyClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PropertyClass"
    class_name: ClassVar[str] = "PropertyClass"
    class_model_uri: ClassVar[URIRef] = LOINC.PropertyClass

    id: Union[str, PropertyClassId] = None
    subClassOf: Optional[Union[Union[str, PropertyClassId], List[Union[str, PropertyClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, PropertyClassId):
            self.id = PropertyClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, PropertyClassId) else PropertyClassId(v) for v in self.subClassOf]

        super().__post_init__(**kwargs)


@dataclass
class ScaleClass(LoincPart):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/ScaleClass"]
    class_class_curie: ClassVar[str] = "loinc:part/ScaleClass"
    class_name: ClassVar[str] = "ScaleClass"
    class_model_uri: ClassVar[URIRef] = LOINC.ScaleClass

    id: Union[str, ScaleClassId] = None
    subClassOf: Optional[Union[Union[str, ScaleClassId], List[Union[str, ScaleClassId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ScaleClassId):
            self.id = ScaleClassId(self.id)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ScaleClassId) else ScaleClassId(v) for v in self.subClassOf]

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
                        model_uri=LOINC.subClassOf, domain=None, range=Optional[Union[Union[str, LoincEntityId], List[Union[str, LoincEntityId]]]])

slots.equivalentClasses = Slot(uri=OWL.equivalentClass, name="equivalentClasses", curie=OWL.curie('equivalentClass'),
                               model_uri=LOINC.equivalentClasses, domain=None, range=Optional[Union[Union[str, LoincEntityId], List[Union[str, LoincEntityId]]]])

slots.codes = Slot(uri=LOINC.codes, name="codes", curie=LOINC.curie('codes'),
                   model_uri=LOINC.codes, domain=None, range=Optional[Union[Union[str, LoincTermId], List[Union[str, LoincTermId]]]])

slots.parts = Slot(uri=LOINC.parts, name="parts", curie=LOINC.curie('parts'),
                   model_uri=LOINC.parts, domain=None, range=Optional[Union[Union[str, PartClassId], List[Union[str, PartClassId]]]])

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

slots.loinc_class = Slot(uri=LOINC.loinc_class, name="loinc_class", curie=LOINC.curie('loinc_class'),
                   model_uri=LOINC.loinc_class, domain=None, range=Optional[str])

slots.loinc_class_type = Slot(uri=LOINC.loinc_class_type, name="loinc_class_type", curie=LOINC.curie('loinc_class_type'),
                   model_uri=LOINC.loinc_class_type, domain=None, range=Optional[str])

slots.has_component = Slot(uri=LOINC.hasComponent, name="has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=LOINC.has_component, domain=None, range=Optional[Union[str, ComponentClassId]])

slots.has_component_analyte = Slot(uri=LOINC.hasComponentAnalyte, name="has_component_analyte", curie=LOINC.curie('hasComponentAnalyte'),
                   model_uri=LOINC.has_component_analyte, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_component_challenge = Slot(uri=LOINC.hasComponentChallenge, name="has_component_challenge", curie=LOINC.curie('hasComponentChallenge'),
                   model_uri=LOINC.has_component_challenge, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_component_count = Slot(uri=LOINC.hasComponentCount, name="has_component_count", curie=LOINC.curie('hasComponentCount'),
                   model_uri=LOINC.has_component_count, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_component_adjustment = Slot(uri=LOINC.hasComponentAdjustment, name="has_component_adjustment", curie=LOINC.curie('hasComponentAdjustment'),
                   model_uri=LOINC.has_component_adjustment, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_property = Slot(uri=LOINC.hasProperty, name="has_property", curie=LOINC.curie('hasProperty'),
                   model_uri=LOINC.has_property, domain=None, range=Optional[Union[str, PropertyClassId]])

slots.has_time = Slot(uri=LOINC.hasTime, name="has_time", curie=LOINC.curie('hasTime'),
                   model_uri=LOINC.has_time, domain=None, range=Optional[Union[str, TimeClassId]])

slots.has_time_core = Slot(uri=LOINC.hasTimeCore, name="has_time_core", curie=LOINC.curie('hasTimeCore'),
                   model_uri=LOINC.has_time_core, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_time_modifier = Slot(uri=LOINC.hasTimeModifier, name="has_time_modifier", curie=LOINC.curie('hasTimeModifier'),
                   model_uri=LOINC.has_time_modifier, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_system = Slot(uri=LOINC.hasSystem, name="has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=LOINC.has_system, domain=None, range=Optional[Union[str, SystemClassId]])

slots.has_system_core = Slot(uri=LOINC.hasSystemCore, name="has_system_core", curie=LOINC.curie('hasSystemCore'),
                   model_uri=LOINC.has_system_core, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_system_super_system = Slot(uri=LOINC.hasSystemSuperSystem, name="has_system_super_system", curie=LOINC.curie('hasSystemSuperSystem'),
                   model_uri=LOINC.has_system_super_system, domain=None, range=Optional[Union[str, PartClassId]])

slots.has_scale = Slot(uri=LOINC.hasScale, name="has_scale", curie=LOINC.curie('hasScale'),
                   model_uri=LOINC.has_scale, domain=None, range=Optional[Union[str, ScaleClassId]])

slots.has_method = Slot(uri=LOINC.hasMethod, name="has_method", curie=LOINC.curie('hasMethod'),
                   model_uri=LOINC.has_method, domain=None, range=Optional[Union[str, MethodClassId]])

slots.semantic_analyte_gene = Slot(uri=LOINC.semanticAnalyteGene, name="semantic_analyte_gene", curie=LOINC.curie('semanticAnalyteGene'),
                   model_uri=LOINC.semantic_analyte_gene, domain=None, range=Optional[Union[str, PartClassId]])

slots.syntax_analyte_core = Slot(uri=LOINC.syntaxAnalyteCore, name="syntax_analyte_core", curie=LOINC.curie('syntaxAnalyteCore'),
                   model_uri=LOINC.syntax_analyte_core, domain=None, range=Optional[Union[str, PartClassId]])

slots.syntax_analyte_suffix = Slot(uri=LOINC.syntaxAnalyteSuffix, name="syntax_analyte_suffix", curie=LOINC.curie('syntaxAnalyteSuffix'),
                   model_uri=LOINC.syntax_analyte_suffix, domain=None, range=Optional[Union[str, PartClassId]])

slots.syntax_analyte_divisor = Slot(uri=LOINC.syntaxAnalyteDivisor, name="syntax_analyte_divisor", curie=LOINC.curie('syntaxAnalyteDivisor'),
                   model_uri=LOINC.syntax_analyte_divisor, domain=None, range=Optional[Union[str, PartClassId]])

slots.syntax_analyte_divisor_suffix = Slot(uri=LOINC.syntaxAnalyteDivisorSuffix, name="syntax_analyte_divisor_suffix", curie=LOINC.curie('syntaxAnalyteDivisorSuffix'),
                   model_uri=LOINC.syntax_analyte_divisor_suffix, domain=None, range=Optional[Union[str, PartClassId]])

slots.syntax_analyte_numerator = Slot(uri=LOINC.syntaxAnalyteNumerator, name="syntax_analyte_numerator", curie=LOINC.curie('syntaxAnalyteNumerator'),
                   model_uri=LOINC.syntax_analyte_numerator, domain=None, range=Optional[Union[str, PartClassId]])

slots.part_type = Slot(uri=LOINC.part_type, name="part_type", curie=LOINC.curie('part_type'),
                   model_uri=LOINC.part_type, domain=None, range=Optional[str])

slots.part_number = Slot(uri=LOINC.part_number, name="part_number", curie=LOINC.curie('part_number'),
                   model_uri=LOINC.part_number, domain=None, range=Optional[str])

slots.part_name = Slot(uri=LOINC.part_name, name="part_name", curie=LOINC.curie('part_name'),
                   model_uri=LOINC.part_name, domain=None, range=Optional[str])

slots.part_display_name = Slot(uri=LOINC.part_display_name, name="part_display_name", curie=LOINC.curie('part_display_name'),
                   model_uri=LOINC.part_display_name, domain=None, range=Optional[str])

slots.LoincCodeClassIntersection_has_component = Slot(uri=LOINC.hasComponent, name="LoincCodeClassIntersection_has_component", curie=LOINC.curie('hasComponent'),
                                                      model_uri=LOINC.LoincCodeClassIntersection_has_component, domain=LoincTermIntersection, range=Optional[Union[str, ComponentClassId]])

slots.LoincCodeClassIntersection_has_property = Slot(uri=LOINC.hasProperty, name="LoincCodeClassIntersection_has_property", curie=LOINC.curie('hasProperty'),
                                                     model_uri=LOINC.LoincCodeClassIntersection_has_property, domain=LoincTermIntersection, range=Optional[Union[str, PropertyClassId]])

slots.LoincCodeClassIntersection_has_time = Slot(uri=LOINC.hasTime, name="LoincCodeClassIntersection_has_time", curie=LOINC.curie('hasTime'),
                                                 model_uri=LOINC.LoincCodeClassIntersection_has_time, domain=LoincTermIntersection, range=Optional[Union[str, TimeClassId]])

slots.LoincCodeClassIntersection_has_system = Slot(uri=LOINC.hasSystem, name="LoincCodeClassIntersection_has_system", curie=LOINC.curie('hasSystem'),
                                                   model_uri=LOINC.LoincCodeClassIntersection_has_system, domain=LoincTermIntersection, range=Optional[Union[str, SystemClassId]])

slots.LoincCodeClassIntersection_has_scale = Slot(uri=LOINC.hasScale, name="LoincCodeClassIntersection_has_scale", curie=LOINC.curie('hasScale'),
                                                  model_uri=LOINC.LoincCodeClassIntersection_has_scale, domain=LoincTermIntersection, range=Optional[Union[str, ScaleClassId]])

slots.LoincCodeClassIntersection_has_method = Slot(uri=LOINC.hasMethod, name="LoincCodeClassIntersection_has_method", curie=LOINC.curie('hasMethod'),
                                                   model_uri=LOINC.LoincCodeClassIntersection_has_method, domain=LoincTermIntersection, range=Optional[Union[str, MethodClassId]])

slots.LoincCodeClassIntersection_has_component_analyte = Slot(uri=LOINC.hasComponentAnalyte, name="LoincCodeClassIntersection_has_component_analyte", curie=LOINC.curie('hasComponentAnalyte'),
                                                              model_uri=LOINC.LoincCodeClassIntersection_has_component_analyte, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_component_challenge = Slot(uri=LOINC.hasComponentChallenge, name="LoincCodeClassIntersection_has_component_challenge", curie=LOINC.curie('hasComponentChallenge'),
                                                                model_uri=LOINC.LoincCodeClassIntersection_has_component_challenge, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_component_count = Slot(uri=LOINC.hasComponentCount, name="LoincCodeClassIntersection_has_component_count", curie=LOINC.curie('hasComponentCount'),
                                                            model_uri=LOINC.LoincCodeClassIntersection_has_component_count, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_component_adjustment = Slot(uri=LOINC.hasComponentAdjustment, name="LoincCodeClassIntersection_has_component_adjustment", curie=LOINC.curie('hasComponentAdjustment'),
                                                                 model_uri=LOINC.LoincCodeClassIntersection_has_component_adjustment, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_time_core = Slot(uri=LOINC.hasTimeCore, name="LoincCodeClassIntersection_has_time_core", curie=LOINC.curie('hasTimeCore'),
                                                      model_uri=LOINC.LoincCodeClassIntersection_has_time_core, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_time_modifier = Slot(uri=LOINC.hasTimeModifier, name="LoincCodeClassIntersection_has_time_modifier", curie=LOINC.curie('hasTimeModifier'),
                                                          model_uri=LOINC.LoincCodeClassIntersection_has_time_modifier, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_system_core = Slot(uri=LOINC.hasSystemCore, name="LoincCodeClassIntersection_has_system_core", curie=LOINC.curie('hasSystemCore'),
                                                        model_uri=LOINC.LoincCodeClassIntersection_has_system_core, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_has_system_super_system = Slot(uri=LOINC.hasSystemSuperSystem, name="LoincCodeClassIntersection_has_system_super_system", curie=LOINC.curie('hasSystemSuperSystem'),
                                                                model_uri=LOINC.LoincCodeClassIntersection_has_system_super_system, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_semantic_analyte_gene = Slot(uri=LOINC.semanticAnalyteGene, name="LoincCodeClassIntersection_semantic_analyte_gene", curie=LOINC.curie('semanticAnalyteGene'),
                                                              model_uri=LOINC.LoincCodeClassIntersection_semantic_analyte_gene, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_syntax_analyte_core = Slot(uri=LOINC.syntaxAnalyteCore, name="LoincCodeClassIntersection_syntax_analyte_core", curie=LOINC.curie('syntaxAnalyteCore'),
                                                            model_uri=LOINC.LoincCodeClassIntersection_syntax_analyte_core, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_syntax_analyte_suffix = Slot(uri=LOINC.syntaxAnalyteSuffix, name="LoincCodeClassIntersection_syntax_analyte_suffix", curie=LOINC.curie('syntaxAnalyteSuffix'),
                                                              model_uri=LOINC.LoincCodeClassIntersection_syntax_analyte_suffix, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_syntax_analyte_divisor = Slot(uri=LOINC.syntaxAnalyteDivisor, name="LoincCodeClassIntersection_syntax_analyte_divisor", curie=LOINC.curie('syntaxAnalyteDivisor'),
                                                               model_uri=LOINC.LoincCodeClassIntersection_syntax_analyte_divisor, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_syntax_analyte_divisor_suffix = Slot(uri=LOINC.syntaxAnalyteDivisorSuffix, name="LoincCodeClassIntersection_syntax_analyte_divisor_suffix", curie=LOINC.curie('syntaxAnalyteDivisorSuffix'),
                                                                      model_uri=LOINC.LoincCodeClassIntersection_syntax_analyte_divisor_suffix, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassIntersection_syntax_analyte_numerator = Slot(uri=LOINC.syntaxAnalyteNumerator, name="LoincCodeClassIntersection_syntax_analyte_numerator", curie=LOINC.curie('syntaxAnalyteNumerator'),
                                                                 model_uri=LOINC.LoincCodeClassIntersection_syntax_analyte_numerator, domain=LoincTermIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component = Slot(uri=LOINC.hasComponent, name="LoincCodeClassNonIntersection_has_component", curie=LOINC.curie('hasComponent'),
                                                         model_uri=LOINC.LoincCodeClassNonIntersection_has_component, domain=LoincTermNonIntersection, range=Optional[Union[str, ComponentClassId]])

slots.LoincCodeClassNonIntersection_has_property = Slot(uri=LOINC.hasProperty, name="LoincCodeClassNonIntersection_has_property", curie=LOINC.curie('hasProperty'),
                                                        model_uri=LOINC.LoincCodeClassNonIntersection_has_property, domain=LoincTermNonIntersection, range=Optional[Union[str, PropertyClassId]])

slots.LoincCodeClassNonIntersection_has_time = Slot(uri=LOINC.hasTime, name="LoincCodeClassNonIntersection_has_time", curie=LOINC.curie('hasTime'),
                                                    model_uri=LOINC.LoincCodeClassNonIntersection_has_time, domain=LoincTermNonIntersection, range=Optional[Union[str, TimeClassId]])

slots.LoincCodeClassNonIntersection_has_system = Slot(uri=LOINC.hasSystem, name="LoincCodeClassNonIntersection_has_system", curie=LOINC.curie('hasSystem'),
                                                      model_uri=LOINC.LoincCodeClassNonIntersection_has_system, domain=LoincTermNonIntersection, range=Optional[Union[str, SystemClassId]])

slots.LoincCodeClassNonIntersection_has_scale = Slot(uri=LOINC.hasScale, name="LoincCodeClassNonIntersection_has_scale", curie=LOINC.curie('hasScale'),
                                                     model_uri=LOINC.LoincCodeClassNonIntersection_has_scale, domain=LoincTermNonIntersection, range=Optional[Union[str, ScaleClassId]])

slots.LoincCodeClassNonIntersection_has_method = Slot(uri=LOINC.hasMethod, name="LoincCodeClassNonIntersection_has_method", curie=LOINC.curie('hasMethod'),
                                                      model_uri=LOINC.LoincCodeClassNonIntersection_has_method, domain=LoincTermNonIntersection, range=Optional[Union[str, MethodClassId]])

slots.LoincCodeClassNonIntersection_has_component_analyte = Slot(uri=LOINC.hasComponentAnalyte, name="LoincCodeClassNonIntersection_has_component_analyte", curie=LOINC.curie('hasComponentAnalyte'),
                                                                 model_uri=LOINC.LoincCodeClassNonIntersection_has_component_analyte, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_challenge = Slot(uri=LOINC.hasComponentChallenge, name="LoincCodeClassNonIntersection_has_component_challenge", curie=LOINC.curie('hasComponentChallenge'),
                                                                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component_challenge, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_count = Slot(uri=LOINC.hasComponentCount, name="LoincCodeClassNonIntersection_has_component_count", curie=LOINC.curie('hasComponentCount'),
                                                               model_uri=LOINC.LoincCodeClassNonIntersection_has_component_count, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_adjustment = Slot(uri=LOINC.hasComponentAdjustment, name="LoincCodeClassNonIntersection_has_component_adjustment", curie=LOINC.curie('hasComponentAdjustment'),
                                                                    model_uri=LOINC.LoincCodeClassNonIntersection_has_component_adjustment, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_time_core = Slot(uri=LOINC.hasTimeCore, name="LoincCodeClassNonIntersection_has_time_core", curie=LOINC.curie('hasTimeCore'),
                                                         model_uri=LOINC.LoincCodeClassNonIntersection_has_time_core, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_time_modifier = Slot(uri=LOINC.hasTimeModifier, name="LoincCodeClassNonIntersection_has_time_modifier", curie=LOINC.curie('hasTimeModifier'),
                                                             model_uri=LOINC.LoincCodeClassNonIntersection_has_time_modifier, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_system_core = Slot(uri=LOINC.hasSystemCore, name="LoincCodeClassNonIntersection_has_system_core", curie=LOINC.curie('hasSystemCore'),
                                                           model_uri=LOINC.LoincCodeClassNonIntersection_has_system_core, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_system_super_system = Slot(uri=LOINC.hasSystemSuperSystem, name="LoincCodeClassNonIntersection_has_system_super_system", curie=LOINC.curie('hasSystemSuperSystem'),
                                                                   model_uri=LOINC.LoincCodeClassNonIntersection_has_system_super_system, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_semantic_analyte_gene = Slot(uri=LOINC.semanticAnalyteGene, name="LoincCodeClassNonIntersection_semantic_analyte_gene", curie=LOINC.curie('semanticAnalyteGene'),
                                                                 model_uri=LOINC.LoincCodeClassNonIntersection_semantic_analyte_gene, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_core = Slot(uri=LOINC.syntaxAnalyteCore, name="LoincCodeClassNonIntersection_syntax_analyte_core", curie=LOINC.curie('syntaxAnalyteCore'),
                                                               model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_core, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_suffix = Slot(uri=LOINC.syntaxAnalyteSuffix, name="LoincCodeClassNonIntersection_syntax_analyte_suffix", curie=LOINC.curie('syntaxAnalyteSuffix'),
                                                                 model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_suffix, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_divisor = Slot(uri=LOINC.syntaxAnalyteDivisor, name="LoincCodeClassNonIntersection_syntax_analyte_divisor", curie=LOINC.curie('syntaxAnalyteDivisor'),
                                                                  model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_divisor, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix = Slot(uri=LOINC.syntaxAnalyteDivisorSuffix, name="LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix", curie=LOINC.curie('syntaxAnalyteDivisorSuffix'),
                                                                         model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_numerator = Slot(uri=LOINC.syntaxAnalyteNumerator, name="LoincCodeClassNonIntersection_syntax_analyte_numerator", curie=LOINC.curie('syntaxAnalyteNumerator'),
                                                                    model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_numerator, domain=LoincTermNonIntersection, range=Optional[Union[str, PartClassId]])

slots.ComponentClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ComponentClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.ComponentClass_subClassOf, domain=ComponentClass, range=Optional[Union[Union[str, ComponentClassId], List[Union[str, ComponentClassId]]]])

slots.SystemClass_subClassOf = Slot(uri=RDFS.subClassOf, name="SystemClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.SystemClass_subClassOf, domain=SystemClass, range=Optional[Union[Union[str, SystemClassId], List[Union[str, SystemClassId]]]])

slots.MethodClass_subClassOf = Slot(uri=RDFS.subClassOf, name="MethodClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.MethodClass_subClassOf, domain=MethodClass, range=Optional[Union[Union[str, MethodClassId], List[Union[str, MethodClassId]]]])

slots.TimeClass_subClassOf = Slot(uri=RDFS.subClassOf, name="TimeClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.TimeClass_subClassOf, domain=TimeClass, range=Optional[Union[Union[str, TimeClassId], List[Union[str, TimeClassId]]]])

slots.PropertyClass_subClassOf = Slot(uri=RDFS.subClassOf, name="PropertyClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.PropertyClass_subClassOf, domain=PropertyClass, range=Optional[Union[Union[str, PropertyClassId], List[Union[str, PropertyClassId]]]])

slots.ScaleClass_subClassOf = Slot(uri=RDFS.subClassOf, name="ScaleClass_subClassOf", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.ScaleClass_subClassOf, domain=ScaleClass, range=Optional[Union[Union[str, ScaleClassId], List[Union[str, ScaleClassId]]]])