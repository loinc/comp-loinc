# Auto generated from comp_loinc.yaml by pythongen.py version: 0.9.0
# Generation date: 2023-09-27T12:25:01
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
class ThingId(URIorCURIE):
    pass


class LoincCodeClassId(ThingId):
    pass


class LoincCodeClassNonIntersectionId(ThingId):
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
    subClassOf: Optional[Union[Union[str, ThingId], List[Union[str, ThingId]]]] = empty_list()
    equivalentClasses: Optional[Union[Union[str, ThingId], List[Union[str, ThingId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, ThingId):
            self.id = ThingId(self.id)

        if self.label is not None and not isinstance(self.label, str):
            self.label = str(self.label)

        if self.description is not None and not isinstance(self.description, str):
            self.description = str(self.description)

        if not isinstance(self.subClassOf, list):
            self.subClassOf = [self.subClassOf] if self.subClassOf is not None else []
        self.subClassOf = [v if isinstance(v, ThingId) else ThingId(v) for v in self.subClassOf]

        if not isinstance(self.equivalentClasses, list):
            self.equivalentClasses = [self.equivalentClasses] if self.equivalentClasses is not None else []
        self.equivalentClasses = [v if isinstance(v, ThingId) else ThingId(v) for v in self.equivalentClasses]

        super().__post_init__(**kwargs)


@dataclass
class LoincCodeClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClass"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClass"
    class_name: ClassVar[str] = "LoincCodeClass"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClass

    id: Union[str, LoincCodeClassId] = None
    loinc_number: Optional[str] = None
    long_common_name: Optional[str] = None
    formal_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
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
        if not isinstance(self.id, LoincCodeClassId):
            self.id = LoincCodeClassId(self.id)

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
class LoincCodeClassNonIntersection(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["code/LoincCodeClassNonIntersection"]
    class_class_curie: ClassVar[str] = "loinc:code/LoincCodeClassNonIntersection"
    class_name: ClassVar[str] = "LoincCodeClassNonIntersection"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincCodeClassNonIntersection

    id: Union[str, LoincCodeClassNonIntersectionId] = None
    loinc_number: Optional[str] = None
    long_common_name: Optional[str] = None
    formal_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
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
        if not isinstance(self.id, LoincCodeClassNonIntersectionId):
            self.id = LoincCodeClassNonIntersectionId(self.id)

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
class PartClass(Thing):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["part/PartClass"]
    class_class_curie: ClassVar[str] = "loinc:part/PartClass"
    class_name: ClassVar[str] = "PartClass"
    class_model_uri: ClassVar[URIRef] = LOINC.PartClass

    id: Union[str, PartClassId] = None
    subClassOf: Optional[Union[Union[str, ThingId], List[Union[str, ThingId]]]] = empty_list()
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
        self.subClassOf = [v if isinstance(v, ThingId) else ThingId(v) for v in self.subClassOf]

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
class ComponentClass(PartClass):
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
class SystemClass(PartClass):
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
class MethodClass(PartClass):
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
class TimeClass(PartClass):
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
class PropertyClass(PartClass):
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
class ScaleClass(PartClass):
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
                   model_uri=LOINC.subClassOf, domain=None, range=Optional[Union[Union[str, ThingId], List[Union[str, ThingId]]]])

slots.equivalentClasses = Slot(uri=OWL.equivalentClass, name="equivalentClasses", curie=OWL.curie('equivalentClass'),
                   model_uri=LOINC.equivalentClasses, domain=None, range=Optional[Union[Union[str, ThingId], List[Union[str, ThingId]]]])

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

slots.LoincCodeClass_has_component = Slot(uri=LOINC.hasComponent, name="LoincCodeClass_has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=LOINC.LoincCodeClass_has_component, domain=LoincCodeClass, range=Optional[Union[str, ComponentClassId]])

slots.LoincCodeClass_has_property = Slot(uri=LOINC.hasProperty, name="LoincCodeClass_has_property", curie=LOINC.curie('hasProperty'),
                   model_uri=LOINC.LoincCodeClass_has_property, domain=LoincCodeClass, range=Optional[Union[str, PropertyClassId]])

slots.LoincCodeClass_has_time = Slot(uri=LOINC.hasTime, name="LoincCodeClass_has_time", curie=LOINC.curie('hasTime'),
                   model_uri=LOINC.LoincCodeClass_has_time, domain=LoincCodeClass, range=Optional[Union[str, TimeClassId]])

slots.LoincCodeClass_has_system = Slot(uri=LOINC.hasSystem, name="LoincCodeClass_has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=LOINC.LoincCodeClass_has_system, domain=LoincCodeClass, range=Optional[Union[str, SystemClassId]])

slots.LoincCodeClass_has_scale = Slot(uri=LOINC.hasScale, name="LoincCodeClass_has_scale", curie=LOINC.curie('hasScale'),
                   model_uri=LOINC.LoincCodeClass_has_scale, domain=LoincCodeClass, range=Optional[Union[str, ScaleClassId]])

slots.LoincCodeClass_has_method = Slot(uri=LOINC.hasMethod, name="LoincCodeClass_has_method", curie=LOINC.curie('hasMethod'),
                   model_uri=LOINC.LoincCodeClass_has_method, domain=LoincCodeClass, range=Optional[Union[str, MethodClassId]])

slots.LoincCodeClass_has_component_analyte = Slot(uri=LOINC.hasComponentAnalyte, name="LoincCodeClass_has_component_analyte", curie=LOINC.curie('hasComponentAnalyte'),
                   model_uri=LOINC.LoincCodeClass_has_component_analyte, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_component_challenge = Slot(uri=LOINC.hasComponentChallenge, name="LoincCodeClass_has_component_challenge", curie=LOINC.curie('hasComponentChallenge'),
                   model_uri=LOINC.LoincCodeClass_has_component_challenge, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_component_count = Slot(uri=LOINC.hasComponentCount, name="LoincCodeClass_has_component_count", curie=LOINC.curie('hasComponentCount'),
                   model_uri=LOINC.LoincCodeClass_has_component_count, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_component_adjustment = Slot(uri=LOINC.hasComponentAdjustment, name="LoincCodeClass_has_component_adjustment", curie=LOINC.curie('hasComponentAdjustment'),
                   model_uri=LOINC.LoincCodeClass_has_component_adjustment, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_time_core = Slot(uri=LOINC.hasTimeCore, name="LoincCodeClass_has_time_core", curie=LOINC.curie('hasTimeCore'),
                   model_uri=LOINC.LoincCodeClass_has_time_core, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_time_modifier = Slot(uri=LOINC.hasTimeModifier, name="LoincCodeClass_has_time_modifier", curie=LOINC.curie('hasTimeModifier'),
                   model_uri=LOINC.LoincCodeClass_has_time_modifier, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_system_core = Slot(uri=LOINC.hasSystemCore, name="LoincCodeClass_has_system_core", curie=LOINC.curie('hasSystemCore'),
                   model_uri=LOINC.LoincCodeClass_has_system_core, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_has_system_super_system = Slot(uri=LOINC.hasSystemSuperSystem, name="LoincCodeClass_has_system_super_system", curie=LOINC.curie('hasSystemSuperSystem'),
                   model_uri=LOINC.LoincCodeClass_has_system_super_system, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_semantic_analyte_gene = Slot(uri=LOINC.semanticAnalyteGene, name="LoincCodeClass_semantic_analyte_gene", curie=LOINC.curie('semanticAnalyteGene'),
                   model_uri=LOINC.LoincCodeClass_semantic_analyte_gene, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_syntax_analyte_core = Slot(uri=LOINC.syntaxAnalyteCore, name="LoincCodeClass_syntax_analyte_core", curie=LOINC.curie('syntaxAnalyteCore'),
                   model_uri=LOINC.LoincCodeClass_syntax_analyte_core, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_syntax_analyte_suffix = Slot(uri=LOINC.syntaxAnalyteSuffix, name="LoincCodeClass_syntax_analyte_suffix", curie=LOINC.curie('syntaxAnalyteSuffix'),
                   model_uri=LOINC.LoincCodeClass_syntax_analyte_suffix, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_syntax_analyte_divisor = Slot(uri=LOINC.syntaxAnalyteDivisor, name="LoincCodeClass_syntax_analyte_divisor", curie=LOINC.curie('syntaxAnalyteDivisor'),
                   model_uri=LOINC.LoincCodeClass_syntax_analyte_divisor, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_syntax_analyte_divisor_suffix = Slot(uri=LOINC.syntaxAnalyteDivisorSuffix, name="LoincCodeClass_syntax_analyte_divisor_suffix", curie=LOINC.curie('syntaxAnalyteDivisorSuffix'),
                   model_uri=LOINC.LoincCodeClass_syntax_analyte_divisor_suffix, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClass_syntax_analyte_numerator = Slot(uri=LOINC.syntaxAnalyteNumerator, name="LoincCodeClass_syntax_analyte_numerator", curie=LOINC.curie('syntaxAnalyteNumerator'),
                   model_uri=LOINC.LoincCodeClass_syntax_analyte_numerator, domain=LoincCodeClass, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component = Slot(uri=LOINC.hasComponent, name="LoincCodeClassNonIntersection_has_component", curie=LOINC.curie('hasComponent'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, ComponentClassId]])

slots.LoincCodeClassNonIntersection_has_property = Slot(uri=LOINC.hasProperty, name="LoincCodeClassNonIntersection_has_property", curie=LOINC.curie('hasProperty'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_property, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PropertyClassId]])

slots.LoincCodeClassNonIntersection_has_time = Slot(uri=LOINC.hasTime, name="LoincCodeClassNonIntersection_has_time", curie=LOINC.curie('hasTime'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_time, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, TimeClassId]])

slots.LoincCodeClassNonIntersection_has_system = Slot(uri=LOINC.hasSystem, name="LoincCodeClassNonIntersection_has_system", curie=LOINC.curie('hasSystem'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_system, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, SystemClassId]])

slots.LoincCodeClassNonIntersection_has_scale = Slot(uri=LOINC.hasScale, name="LoincCodeClassNonIntersection_has_scale", curie=LOINC.curie('hasScale'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_scale, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, ScaleClassId]])

slots.LoincCodeClassNonIntersection_has_method = Slot(uri=LOINC.hasMethod, name="LoincCodeClassNonIntersection_has_method", curie=LOINC.curie('hasMethod'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_method, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, MethodClassId]])

slots.LoincCodeClassNonIntersection_has_component_analyte = Slot(uri=LOINC.hasComponentAnalyte, name="LoincCodeClassNonIntersection_has_component_analyte", curie=LOINC.curie('hasComponentAnalyte'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component_analyte, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_challenge = Slot(uri=LOINC.hasComponentChallenge, name="LoincCodeClassNonIntersection_has_component_challenge", curie=LOINC.curie('hasComponentChallenge'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component_challenge, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_count = Slot(uri=LOINC.hasComponentCount, name="LoincCodeClassNonIntersection_has_component_count", curie=LOINC.curie('hasComponentCount'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component_count, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_component_adjustment = Slot(uri=LOINC.hasComponentAdjustment, name="LoincCodeClassNonIntersection_has_component_adjustment", curie=LOINC.curie('hasComponentAdjustment'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_component_adjustment, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_time_core = Slot(uri=LOINC.hasTimeCore, name="LoincCodeClassNonIntersection_has_time_core", curie=LOINC.curie('hasTimeCore'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_time_core, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_time_modifier = Slot(uri=LOINC.hasTimeModifier, name="LoincCodeClassNonIntersection_has_time_modifier", curie=LOINC.curie('hasTimeModifier'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_time_modifier, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_system_core = Slot(uri=LOINC.hasSystemCore, name="LoincCodeClassNonIntersection_has_system_core", curie=LOINC.curie('hasSystemCore'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_system_core, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_has_system_super_system = Slot(uri=LOINC.hasSystemSuperSystem, name="LoincCodeClassNonIntersection_has_system_super_system", curie=LOINC.curie('hasSystemSuperSystem'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_has_system_super_system, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_semantic_analyte_gene = Slot(uri=LOINC.semanticAnalyteGene, name="LoincCodeClassNonIntersection_semantic_analyte_gene", curie=LOINC.curie('semanticAnalyteGene'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_semantic_analyte_gene, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_core = Slot(uri=LOINC.syntaxAnalyteCore, name="LoincCodeClassNonIntersection_syntax_analyte_core", curie=LOINC.curie('syntaxAnalyteCore'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_core, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_suffix = Slot(uri=LOINC.syntaxAnalyteSuffix, name="LoincCodeClassNonIntersection_syntax_analyte_suffix", curie=LOINC.curie('syntaxAnalyteSuffix'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_suffix, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_divisor = Slot(uri=LOINC.syntaxAnalyteDivisor, name="LoincCodeClassNonIntersection_syntax_analyte_divisor", curie=LOINC.curie('syntaxAnalyteDivisor'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_divisor, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix = Slot(uri=LOINC.syntaxAnalyteDivisorSuffix, name="LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix", curie=LOINC.curie('syntaxAnalyteDivisorSuffix'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_divisor_suffix, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

slots.LoincCodeClassNonIntersection_syntax_analyte_numerator = Slot(uri=LOINC.syntaxAnalyteNumerator, name="LoincCodeClassNonIntersection_syntax_analyte_numerator", curie=LOINC.curie('syntaxAnalyteNumerator'),
                   model_uri=LOINC.LoincCodeClassNonIntersection_syntax_analyte_numerator, domain=LoincCodeClassNonIntersection, range=Optional[Union[str, PartClassId]])

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
