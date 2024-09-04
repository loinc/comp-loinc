# Auto generated from comp_loinc.yaml by pythongen.py version: 0.0.1
# Generation date: 2024-09-03T12:09:49
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
from datetime import date, datetime
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
LOINC_PROPERTY = CurieNamespace('loinc_property', 'http://loinc.org/property/')
OWL = CurieNamespace('owl', 'http://www.w3.org/2002/07/owl#')
RDFS = CurieNamespace('rdfs', 'http://www.w3.org/2000/01/rdf-schema#')
SCT = CurieNamespace('sct', 'http://snomed.info/sct')
DEFAULT_ = LOINC


# Types

# Class references
class EntityId(URIorCURIE):
    pass


class SnomedConceptId(EntityId):
    pass


class LoincEntityId(EntityId):
    pass


class LoincTermId(LoincEntityId):
    pass


class LoincPartId(LoincEntityId):
    pass


@dataclass
class Loinc(YAMLRoot):
    """
    A container of Loinc term and part instances.
    """
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Class"]
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Loinc"
    class_model_uri: ClassVar[URIRef] = LOINC.Loinc

    codes: Optional[Union[Union[str, LoincTermId], List[Union[str, LoincTermId]]]] = empty_list()
    parts: Optional[Union[Union[str, LoincPartId], List[Union[str, LoincPartId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if not isinstance(self.codes, list):
            self.codes = [self.codes] if self.codes is not None else []
        self.codes = [v if isinstance(v, LoincTermId) else LoincTermId(v) for v in self.codes]

        if not isinstance(self.parts, list):
            self.parts = [self.parts] if self.parts is not None else []
        self.parts = [v if isinstance(v, LoincPartId) else LoincPartId(v) for v in self.parts]

        super().__post_init__(**kwargs)


@dataclass
class Entity(YAMLRoot):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = OWL["Class"]
    class_class_curie: ClassVar[str] = "owl:Class"
    class_name: ClassVar[str] = "Entity"
    class_model_uri: ClassVar[URIRef] = LOINC.Entity

    id: Union[str, EntityId] = None
    entity_label: Optional[str] = None
    entity_description: Optional[str] = None
    sub_class_of: Optional[Union[Union[str, EntityId], List[Union[str, EntityId]]]] = empty_list()
    equivalent_class: Optional[Union[Union[str, EntityId], List[Union[str, EntityId]]]] = empty_list()

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, EntityId):
            self.id = EntityId(self.id)

        if self.entity_label is not None and not isinstance(self.entity_label, str):
            self.entity_label = str(self.entity_label)

        if self.entity_description is not None and not isinstance(self.entity_description, str):
            self.entity_description = str(self.entity_description)

        if not isinstance(self.sub_class_of, list):
            self.sub_class_of = [self.sub_class_of] if self.sub_class_of is not None else []
        self.sub_class_of = [v if isinstance(v, EntityId) else EntityId(v) for v in self.sub_class_of]

        if not isinstance(self.equivalent_class, list):
            self.equivalent_class = [self.equivalent_class] if self.equivalent_class is not None else []
        self.equivalent_class = [v if isinstance(v, EntityId) else EntityId(v) for v in self.equivalent_class]

        super().__post_init__(**kwargs)


@dataclass
class SnomedConcept(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = SCT["SnomedConcept"]
    class_class_curie: ClassVar[str] = "sct:SnomedConcept"
    class_name: ClassVar[str] = "SnomedConcept"
    class_model_uri: ClassVar[URIRef] = LOINC.SnomedConcept

    id: Union[str, SnomedConceptId] = None
    fully_specified_name: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, SnomedConceptId):
            self.id = SnomedConceptId(self.id)

        if self.fully_specified_name is not None and not isinstance(self.fully_specified_name, str):
            self.fully_specified_name = str(self.fully_specified_name)

        super().__post_init__(**kwargs)


@dataclass
class LoincEntity(Entity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["LoincEntity"]
    class_class_curie: ClassVar[str] = "loinc:LoincEntity"
    class_name: ClassVar[str] = "LoincEntity"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincEntity

    id: Union[str, LoincEntityId] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincEntityId):
            self.id = LoincEntityId(self.id)

        super().__post_init__(**kwargs)


@dataclass
class LoincTerm(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["LoincTerm"]
    class_class_curie: ClassVar[str] = "loinc:LoincTerm"
    class_name: ClassVar[str] = "LoincTerm"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincTerm

    id: Union[str, LoincTermId] = None
    loinc_number: Optional[str] = None
    long_common_name: Optional[str] = None
    short_name: Optional[str] = None
    status: Optional[str] = None
    loinc_class: Optional[str] = None
    loinc_class_type: Optional[str] = None
    primary_component: Optional[Union[str, LoincPartId]] = None
    primary_property: Optional[Union[str, LoincPartId]] = None
    supplementary_property: Optional[Union[str, LoincPartId]] = None
    primary_time_aspect: Optional[Union[str, LoincPartId]] = None
    primary_system: Optional[Union[str, LoincPartId]] = None
    primary_scale_typ: Optional[Union[str, LoincPartId]] = None
    supplementary_scale_typ: Optional[Union[str, LoincPartId]] = None
    primary_method_typ: Optional[Union[str, LoincPartId]] = None
    supplementary_method_typ: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte: Optional[Union[str, LoincPartId]] = None
    supplementary_challenge: Optional[Union[str, LoincPartId]] = None
    supplementary_adjustment: Optional[Union[str, LoincPartId]] = None
    supplementary_count: Optional[Union[str, LoincPartId]] = None
    supplementary_time_core: Optional[Union[str, LoincPartId]] = None
    supplementary_time_modifier: Optional[Union[str, LoincPartId]] = None
    supplementary_system_core: Optional[Union[str, LoincPartId]] = None
    supplementary_super_system: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_core: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_suffix: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_numerator: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_divisor: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_divisor_suffix: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_gene: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_genetic_variant: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_chemical: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_divisor_chemical: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_clinical_drug: Optional[Union[str, LoincPartId]] = None
    supplementary_system_core_anatomic_entity: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_organism: Optional[Union[str, LoincPartId]] = None
    supplementary_challenge_route: Optional[Union[str, LoincPartId]] = None
    supplementary_analyte_allergen: Optional[Union[str, LoincPartId]] = None
    supplementary_class: Optional[Union[str, LoincPartId]] = None
    supplementary_category: Optional[Union[str, LoincPartId]] = None
    supplementary_search: Optional[Union[str, LoincPartId]] = None
    primary_rad_anatomic_location_imaging_focus: Optional[Union[str, LoincPartId]] = None
    primary_rad_anatomic_location_laterality: Optional[Union[str, LoincPartId]] = None
    primary_rad_anatomic_location_laterality_presence: Optional[Union[str, LoincPartId]] = None
    primary_rad_anatomic_location_region_imaged: Optional[Union[str, LoincPartId]] = None
    primary_rad_guidance_for_action: Optional[Union[str, LoincPartId]] = None
    primary_rad_guidance_for_approach: Optional[Union[str, LoincPartId]] = None
    primary_rad_guidance_for_object: Optional[Union[str, LoincPartId]] = None
    primary_rad_guidance_for_presence: Optional[Union[str, LoincPartId]] = None
    primary_rad_maneuver_maneuver_type: Optional[Union[str, LoincPartId]] = None
    primary_rad_modality_subtype: Optional[Union[str, LoincPartId]] = None
    primary_rad_modality_type: Optional[Union[str, LoincPartId]] = None
    primary_rad_pharmaceutical_route: Optional[Union[str, LoincPartId]] = None
    primary_rad_pharmaceutical_substance_given: Optional[Union[str, LoincPartId]] = None
    primary_rad_reason_for_exam: Optional[Union[str, LoincPartId]] = None
    primary_rad_subject: Optional[Union[str, LoincPartId]] = None
    primary_rad_timing: Optional[Union[str, LoincPartId]] = None
    primary_rad_view_aggregation: Optional[Union[str, LoincPartId]] = None
    primary_rad_view_view_type: Optional[Union[str, LoincPartId]] = None
    primary_document_kind: Optional[Union[str, LoincPartId]] = None
    primary_document_role: Optional[Union[str, LoincPartId]] = None
    primary_document_setting: Optional[Union[str, LoincPartId]] = None
    primary_document_subject_matter_domain: Optional[Union[str, LoincPartId]] = None
    primary_document_type_of_service: Optional[Union[str, LoincPartId]] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincTermId):
            self.id = LoincTermId(self.id)

        if self.loinc_number is not None and not isinstance(self.loinc_number, str):
            self.loinc_number = str(self.loinc_number)

        if self.long_common_name is not None and not isinstance(self.long_common_name, str):
            self.long_common_name = str(self.long_common_name)

        if self.short_name is not None and not isinstance(self.short_name, str):
            self.short_name = str(self.short_name)

        if self.status is not None and not isinstance(self.status, str):
            self.status = str(self.status)

        if self.loinc_class is not None and not isinstance(self.loinc_class, str):
            self.loinc_class = str(self.loinc_class)

        if self.loinc_class_type is not None and not isinstance(self.loinc_class_type, str):
            self.loinc_class_type = str(self.loinc_class_type)

        if self.primary_component is not None and not isinstance(self.primary_component, LoincPartId):
            self.primary_component = LoincPartId(self.primary_component)

        if self.primary_property is not None and not isinstance(self.primary_property, LoincPartId):
            self.primary_property = LoincPartId(self.primary_property)

        if self.supplementary_property is not None and not isinstance(self.supplementary_property, LoincPartId):
            self.supplementary_property = LoincPartId(self.supplementary_property)

        if self.primary_time_aspect is not None and not isinstance(self.primary_time_aspect, LoincPartId):
            self.primary_time_aspect = LoincPartId(self.primary_time_aspect)

        if self.primary_system is not None and not isinstance(self.primary_system, LoincPartId):
            self.primary_system = LoincPartId(self.primary_system)

        if self.primary_scale_typ is not None and not isinstance(self.primary_scale_typ, LoincPartId):
            self.primary_scale_typ = LoincPartId(self.primary_scale_typ)

        if self.supplementary_scale_typ is not None and not isinstance(self.supplementary_scale_typ, LoincPartId):
            self.supplementary_scale_typ = LoincPartId(self.supplementary_scale_typ)

        if self.primary_method_typ is not None and not isinstance(self.primary_method_typ, LoincPartId):
            self.primary_method_typ = LoincPartId(self.primary_method_typ)

        if self.supplementary_method_typ is not None and not isinstance(self.supplementary_method_typ, LoincPartId):
            self.supplementary_method_typ = LoincPartId(self.supplementary_method_typ)

        if self.supplementary_analyte is not None and not isinstance(self.supplementary_analyte, LoincPartId):
            self.supplementary_analyte = LoincPartId(self.supplementary_analyte)

        if self.supplementary_challenge is not None and not isinstance(self.supplementary_challenge, LoincPartId):
            self.supplementary_challenge = LoincPartId(self.supplementary_challenge)

        if self.supplementary_adjustment is not None and not isinstance(self.supplementary_adjustment, LoincPartId):
            self.supplementary_adjustment = LoincPartId(self.supplementary_adjustment)

        if self.supplementary_count is not None and not isinstance(self.supplementary_count, LoincPartId):
            self.supplementary_count = LoincPartId(self.supplementary_count)

        if self.supplementary_time_core is not None and not isinstance(self.supplementary_time_core, LoincPartId):
            self.supplementary_time_core = LoincPartId(self.supplementary_time_core)

        if self.supplementary_time_modifier is not None and not isinstance(self.supplementary_time_modifier, LoincPartId):
            self.supplementary_time_modifier = LoincPartId(self.supplementary_time_modifier)

        if self.supplementary_system_core is not None and not isinstance(self.supplementary_system_core, LoincPartId):
            self.supplementary_system_core = LoincPartId(self.supplementary_system_core)

        if self.supplementary_super_system is not None and not isinstance(self.supplementary_super_system, LoincPartId):
            self.supplementary_super_system = LoincPartId(self.supplementary_super_system)

        if self.supplementary_analyte_core is not None and not isinstance(self.supplementary_analyte_core, LoincPartId):
            self.supplementary_analyte_core = LoincPartId(self.supplementary_analyte_core)

        if self.supplementary_analyte_suffix is not None and not isinstance(self.supplementary_analyte_suffix, LoincPartId):
            self.supplementary_analyte_suffix = LoincPartId(self.supplementary_analyte_suffix)

        if self.supplementary_analyte_numerator is not None and not isinstance(self.supplementary_analyte_numerator, LoincPartId):
            self.supplementary_analyte_numerator = LoincPartId(self.supplementary_analyte_numerator)

        if self.supplementary_analyte_divisor is not None and not isinstance(self.supplementary_analyte_divisor, LoincPartId):
            self.supplementary_analyte_divisor = LoincPartId(self.supplementary_analyte_divisor)

        if self.supplementary_analyte_divisor_suffix is not None and not isinstance(self.supplementary_analyte_divisor_suffix, LoincPartId):
            self.supplementary_analyte_divisor_suffix = LoincPartId(self.supplementary_analyte_divisor_suffix)

        if self.supplementary_analyte_gene is not None and not isinstance(self.supplementary_analyte_gene, LoincPartId):
            self.supplementary_analyte_gene = LoincPartId(self.supplementary_analyte_gene)

        if self.supplementary_analyte_genetic_variant is not None and not isinstance(self.supplementary_analyte_genetic_variant, LoincPartId):
            self.supplementary_analyte_genetic_variant = LoincPartId(self.supplementary_analyte_genetic_variant)

        if self.supplementary_analyte_chemical is not None and not isinstance(self.supplementary_analyte_chemical, LoincPartId):
            self.supplementary_analyte_chemical = LoincPartId(self.supplementary_analyte_chemical)

        if self.supplementary_analyte_divisor_chemical is not None and not isinstance(self.supplementary_analyte_divisor_chemical, LoincPartId):
            self.supplementary_analyte_divisor_chemical = LoincPartId(self.supplementary_analyte_divisor_chemical)

        if self.supplementary_analyte_clinical_drug is not None and not isinstance(self.supplementary_analyte_clinical_drug, LoincPartId):
            self.supplementary_analyte_clinical_drug = LoincPartId(self.supplementary_analyte_clinical_drug)

        if self.supplementary_system_core_anatomic_entity is not None and not isinstance(self.supplementary_system_core_anatomic_entity, LoincPartId):
            self.supplementary_system_core_anatomic_entity = LoincPartId(self.supplementary_system_core_anatomic_entity)

        if self.supplementary_analyte_organism is not None and not isinstance(self.supplementary_analyte_organism, LoincPartId):
            self.supplementary_analyte_organism = LoincPartId(self.supplementary_analyte_organism)

        if self.supplementary_challenge_route is not None and not isinstance(self.supplementary_challenge_route, LoincPartId):
            self.supplementary_challenge_route = LoincPartId(self.supplementary_challenge_route)

        if self.supplementary_analyte_allergen is not None and not isinstance(self.supplementary_analyte_allergen, LoincPartId):
            self.supplementary_analyte_allergen = LoincPartId(self.supplementary_analyte_allergen)

        if self.supplementary_class is not None and not isinstance(self.supplementary_class, LoincPartId):
            self.supplementary_class = LoincPartId(self.supplementary_class)

        if self.supplementary_category is not None and not isinstance(self.supplementary_category, LoincPartId):
            self.supplementary_category = LoincPartId(self.supplementary_category)

        if self.supplementary_search is not None and not isinstance(self.supplementary_search, LoincPartId):
            self.supplementary_search = LoincPartId(self.supplementary_search)

        if self.primary_rad_anatomic_location_imaging_focus is not None and not isinstance(self.primary_rad_anatomic_location_imaging_focus, LoincPartId):
            self.primary_rad_anatomic_location_imaging_focus = LoincPartId(self.primary_rad_anatomic_location_imaging_focus)

        if self.primary_rad_anatomic_location_laterality is not None and not isinstance(self.primary_rad_anatomic_location_laterality, LoincPartId):
            self.primary_rad_anatomic_location_laterality = LoincPartId(self.primary_rad_anatomic_location_laterality)

        if self.primary_rad_anatomic_location_laterality_presence is not None and not isinstance(self.primary_rad_anatomic_location_laterality_presence, LoincPartId):
            self.primary_rad_anatomic_location_laterality_presence = LoincPartId(self.primary_rad_anatomic_location_laterality_presence)

        if self.primary_rad_anatomic_location_region_imaged is not None and not isinstance(self.primary_rad_anatomic_location_region_imaged, LoincPartId):
            self.primary_rad_anatomic_location_region_imaged = LoincPartId(self.primary_rad_anatomic_location_region_imaged)

        if self.primary_rad_guidance_for_action is not None and not isinstance(self.primary_rad_guidance_for_action, LoincPartId):
            self.primary_rad_guidance_for_action = LoincPartId(self.primary_rad_guidance_for_action)

        if self.primary_rad_guidance_for_approach is not None and not isinstance(self.primary_rad_guidance_for_approach, LoincPartId):
            self.primary_rad_guidance_for_approach = LoincPartId(self.primary_rad_guidance_for_approach)

        if self.primary_rad_guidance_for_object is not None and not isinstance(self.primary_rad_guidance_for_object, LoincPartId):
            self.primary_rad_guidance_for_object = LoincPartId(self.primary_rad_guidance_for_object)

        if self.primary_rad_guidance_for_presence is not None and not isinstance(self.primary_rad_guidance_for_presence, LoincPartId):
            self.primary_rad_guidance_for_presence = LoincPartId(self.primary_rad_guidance_for_presence)

        if self.primary_rad_maneuver_maneuver_type is not None and not isinstance(self.primary_rad_maneuver_maneuver_type, LoincPartId):
            self.primary_rad_maneuver_maneuver_type = LoincPartId(self.primary_rad_maneuver_maneuver_type)

        if self.primary_rad_modality_subtype is not None and not isinstance(self.primary_rad_modality_subtype, LoincPartId):
            self.primary_rad_modality_subtype = LoincPartId(self.primary_rad_modality_subtype)

        if self.primary_rad_modality_type is not None and not isinstance(self.primary_rad_modality_type, LoincPartId):
            self.primary_rad_modality_type = LoincPartId(self.primary_rad_modality_type)

        if self.primary_rad_pharmaceutical_route is not None and not isinstance(self.primary_rad_pharmaceutical_route, LoincPartId):
            self.primary_rad_pharmaceutical_route = LoincPartId(self.primary_rad_pharmaceutical_route)

        if self.primary_rad_pharmaceutical_substance_given is not None and not isinstance(self.primary_rad_pharmaceutical_substance_given, LoincPartId):
            self.primary_rad_pharmaceutical_substance_given = LoincPartId(self.primary_rad_pharmaceutical_substance_given)

        if self.primary_rad_reason_for_exam is not None and not isinstance(self.primary_rad_reason_for_exam, LoincPartId):
            self.primary_rad_reason_for_exam = LoincPartId(self.primary_rad_reason_for_exam)

        if self.primary_rad_subject is not None and not isinstance(self.primary_rad_subject, LoincPartId):
            self.primary_rad_subject = LoincPartId(self.primary_rad_subject)

        if self.primary_rad_timing is not None and not isinstance(self.primary_rad_timing, LoincPartId):
            self.primary_rad_timing = LoincPartId(self.primary_rad_timing)

        if self.primary_rad_view_aggregation is not None and not isinstance(self.primary_rad_view_aggregation, LoincPartId):
            self.primary_rad_view_aggregation = LoincPartId(self.primary_rad_view_aggregation)

        if self.primary_rad_view_view_type is not None and not isinstance(self.primary_rad_view_view_type, LoincPartId):
            self.primary_rad_view_view_type = LoincPartId(self.primary_rad_view_view_type)

        if self.primary_document_kind is not None and not isinstance(self.primary_document_kind, LoincPartId):
            self.primary_document_kind = LoincPartId(self.primary_document_kind)

        if self.primary_document_role is not None and not isinstance(self.primary_document_role, LoincPartId):
            self.primary_document_role = LoincPartId(self.primary_document_role)

        if self.primary_document_setting is not None and not isinstance(self.primary_document_setting, LoincPartId):
            self.primary_document_setting = LoincPartId(self.primary_document_setting)

        if self.primary_document_subject_matter_domain is not None and not isinstance(self.primary_document_subject_matter_domain, LoincPartId):
            self.primary_document_subject_matter_domain = LoincPartId(self.primary_document_subject_matter_domain)

        if self.primary_document_type_of_service is not None and not isinstance(self.primary_document_type_of_service, LoincPartId):
            self.primary_document_type_of_service = LoincPartId(self.primary_document_type_of_service)

        super().__post_init__(**kwargs)


@dataclass
class LoincPart(LoincEntity):
    _inherited_slots: ClassVar[List[str]] = []

    class_class_uri: ClassVar[URIRef] = LOINC["LoincPart"]
    class_class_curie: ClassVar[str] = "loinc:LoincPart"
    class_name: ClassVar[str] = "LoincPart"
    class_model_uri: ClassVar[URIRef] = LOINC.LoincPart

    id: Union[str, LoincPartId] = None
    part_number: Optional[str] = None
    part_type_name: Optional[str] = None
    part_name: Optional[str] = None
    part_display_name: Optional[str] = None
    part_status: Optional[str] = None

    def __post_init__(self, *_: List[str], **kwargs: Dict[str, Any]):
        if self._is_empty(self.id):
            self.MissingRequiredField("id")
        if not isinstance(self.id, LoincPartId):
            self.id = LoincPartId(self.id)

        if self.part_number is not None and not isinstance(self.part_number, str):
            self.part_number = str(self.part_number)

        if self.part_type_name is not None and not isinstance(self.part_type_name, str):
            self.part_type_name = str(self.part_type_name)

        if self.part_name is not None and not isinstance(self.part_name, str):
            self.part_name = str(self.part_name)

        if self.part_display_name is not None and not isinstance(self.part_display_name, str):
            self.part_display_name = str(self.part_display_name)

        if self.part_status is not None and not isinstance(self.part_status, str):
            self.part_status = str(self.part_status)

        super().__post_init__(**kwargs)


# Enumerations


# Slots
class slots:
    pass

slots.loinc__codes = Slot(uri=LOINC.codes, name="loinc__codes", curie=LOINC.curie('codes'),
                   model_uri=LOINC.loinc__codes, domain=None, range=Optional[Union[Union[str, LoincTermId], List[Union[str, LoincTermId]]]])

slots.loinc__parts = Slot(uri=LOINC.parts, name="loinc__parts", curie=LOINC.curie('parts'),
                   model_uri=LOINC.loinc__parts, domain=None, range=Optional[Union[Union[str, LoincPartId], List[Union[str, LoincPartId]]]])

slots.entity__id = Slot(uri=LOINC.id, name="entity__id", curie=LOINC.curie('id'),
                   model_uri=LOINC.entity__id, domain=None, range=URIRef)

slots.entity__entity_label = Slot(uri=RDFS.label, name="entity__entity_label", curie=RDFS.curie('label'),
                   model_uri=LOINC.entity__entity_label, domain=None, range=Optional[str])

slots.entity__entity_description = Slot(uri=RDFS.description, name="entity__entity_description", curie=RDFS.curie('description'),
                   model_uri=LOINC.entity__entity_description, domain=None, range=Optional[str])

slots.entity__sub_class_of = Slot(uri=RDFS.subClassOf, name="entity__sub_class_of", curie=RDFS.curie('subClassOf'),
                   model_uri=LOINC.entity__sub_class_of, domain=None, range=Optional[Union[Union[str, EntityId], List[Union[str, EntityId]]]])

slots.entity__equivalent_class = Slot(uri=OWL.equivalentClass, name="entity__equivalent_class", curie=OWL.curie('equivalentClass'),
                   model_uri=LOINC.entity__equivalent_class, domain=None, range=Optional[Union[Union[str, EntityId], List[Union[str, EntityId]]]])

slots.snomedConcept__fully_specified_name = Slot(uri=SCT.fully_specified_name, name="snomedConcept__fully_specified_name", curie=SCT.curie('fully_specified_name'),
                   model_uri=LOINC.snomedConcept__fully_specified_name, domain=None, range=Optional[str])

slots.loincTerm__loinc_number = Slot(uri=LOINC.loinc_number, name="loincTerm__loinc_number", curie=LOINC.curie('loinc_number'),
                   model_uri=LOINC.loincTerm__loinc_number, domain=None, range=Optional[str])

slots.loincTerm__long_common_name = Slot(uri=LOINC.long_common_name, name="loincTerm__long_common_name", curie=LOINC.curie('long_common_name'),
                   model_uri=LOINC.loincTerm__long_common_name, domain=None, range=Optional[str])

slots.loincTerm__short_name = Slot(uri=LOINC.short_name, name="loincTerm__short_name", curie=LOINC.curie('short_name'),
                   model_uri=LOINC.loincTerm__short_name, domain=None, range=Optional[str])

slots.loincTerm__status = Slot(uri=LOINC.status, name="loincTerm__status", curie=LOINC.curie('status'),
                   model_uri=LOINC.loincTerm__status, domain=None, range=Optional[str])

slots.loincTerm__loinc_class = Slot(uri=LOINC.loinc_class, name="loincTerm__loinc_class", curie=LOINC.curie('loinc_class'),
                   model_uri=LOINC.loincTerm__loinc_class, domain=None, range=Optional[str])

slots.loincTerm__loinc_class_type = Slot(uri=LOINC.loinc_class_type, name="loincTerm__loinc_class_type", curie=LOINC.curie('loinc_class_type'),
                   model_uri=LOINC.loincTerm__loinc_class_type, domain=None, range=Optional[str])

slots.loincTerm__primary_component = Slot(uri=LOINC_PROPERTY.COMPONENT, name="loincTerm__primary_component", curie=LOINC_PROPERTY.curie('COMPONENT'),
                   model_uri=LOINC.loincTerm__primary_component, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_property = Slot(uri=LOINC_PROPERTY.PROPERTY, name="loincTerm__primary_property", curie=LOINC_PROPERTY.curie('PROPERTY'),
                   model_uri=LOINC.loincTerm__primary_property, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_property = Slot(uri=LOINC_PROPERTY.PROPERTY, name="loincTerm__supplementary_property", curie=LOINC_PROPERTY.curie('PROPERTY'),
                   model_uri=LOINC.loincTerm__supplementary_property, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_time_aspect = Slot(uri=LOINC_PROPERTY.TIME_ASPECT, name="loincTerm__primary_time_aspect", curie=LOINC_PROPERTY.curie('TIME_ASPECT'),
                   model_uri=LOINC.loincTerm__primary_time_aspect, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_system = Slot(uri=LOINC_PROPERTY.SYSTEM, name="loincTerm__primary_system", curie=LOINC_PROPERTY.curie('SYSTEM'),
                   model_uri=LOINC.loincTerm__primary_system, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_scale_typ = Slot(uri=LOINC_PROPERTY.SCALE_TYP, name="loincTerm__primary_scale_typ", curie=LOINC_PROPERTY.curie('SCALE_TYP'),
                   model_uri=LOINC.loincTerm__primary_scale_typ, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_scale_typ = Slot(uri=LOINC_PROPERTY.SCALE_TYP, name="loincTerm__supplementary_scale_typ", curie=LOINC_PROPERTY.curie('SCALE_TYP'),
                   model_uri=LOINC.loincTerm__supplementary_scale_typ, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_method_typ = Slot(uri=LOINC_PROPERTY.METHOD_TYP, name="loincTerm__primary_method_typ", curie=LOINC_PROPERTY.curie('METHOD_TYP'),
                   model_uri=LOINC.loincTerm__primary_method_typ, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_method_typ = Slot(uri=LOINC_PROPERTY.METHOD_TYP, name="loincTerm__supplementary_method_typ", curie=LOINC_PROPERTY.curie('METHOD_TYP'),
                   model_uri=LOINC.loincTerm__supplementary_method_typ, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte = Slot(uri=LOINC_PROPERTY.analyte, name="loincTerm__supplementary_analyte", curie=LOINC_PROPERTY.curie('analyte'),
                   model_uri=LOINC.loincTerm__supplementary_analyte, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_challenge = Slot(uri=LOINC_PROPERTY.challenge, name="loincTerm__supplementary_challenge", curie=LOINC_PROPERTY.curie('challenge'),
                   model_uri=LOINC.loincTerm__supplementary_challenge, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_adjustment = Slot(uri=LOINC_PROPERTY.adjustment, name="loincTerm__supplementary_adjustment", curie=LOINC_PROPERTY.curie('adjustment'),
                   model_uri=LOINC.loincTerm__supplementary_adjustment, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_count = Slot(uri=LOINC_PROPERTY.count, name="loincTerm__supplementary_count", curie=LOINC_PROPERTY.curie('count'),
                   model_uri=LOINC.loincTerm__supplementary_count, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_time_core = Slot(uri=LOINC_PROPERTY['time-core'], name="loincTerm__supplementary_time_core", curie=LOINC_PROPERTY.curie('time-core'),
                   model_uri=LOINC.loincTerm__supplementary_time_core, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_time_modifier = Slot(uri=LOINC_PROPERTY['time-modifier'], name="loincTerm__supplementary_time_modifier", curie=LOINC_PROPERTY.curie('time-modifier'),
                   model_uri=LOINC.loincTerm__supplementary_time_modifier, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_system_core = Slot(uri=LOINC_PROPERTY['system-core'], name="loincTerm__supplementary_system_core", curie=LOINC_PROPERTY.curie('system-core'),
                   model_uri=LOINC.loincTerm__supplementary_system_core, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_super_system = Slot(uri=LOINC_PROPERTY['super-system'], name="loincTerm__supplementary_super_system", curie=LOINC_PROPERTY.curie('super-system'),
                   model_uri=LOINC.loincTerm__supplementary_super_system, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_core = Slot(uri=LOINC_PROPERTY['analyte-core'], name="loincTerm__supplementary_analyte_core", curie=LOINC_PROPERTY.curie('analyte-core'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_core, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_suffix = Slot(uri=LOINC_PROPERTY['analyte-suffix'], name="loincTerm__supplementary_analyte_suffix", curie=LOINC_PROPERTY.curie('analyte-suffix'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_suffix, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_numerator = Slot(uri=LOINC_PROPERTY['analyte-numerator'], name="loincTerm__supplementary_analyte_numerator", curie=LOINC_PROPERTY.curie('analyte-numerator'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_numerator, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_divisor = Slot(uri=LOINC_PROPERTY['analyte-divisor'], name="loincTerm__supplementary_analyte_divisor", curie=LOINC_PROPERTY.curie('analyte-divisor'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_divisor, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_divisor_suffix = Slot(uri=LOINC_PROPERTY['analyte-divisor-suffix'], name="loincTerm__supplementary_analyte_divisor_suffix", curie=LOINC_PROPERTY.curie('analyte-divisor-suffix'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_divisor_suffix, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_gene = Slot(uri=LOINC_PROPERTY.analyte_gene, name="loincTerm__supplementary_analyte_gene", curie=LOINC_PROPERTY.curie('analyte_gene'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_gene, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_genetic_variant = Slot(uri=LOINC_PROPERTY['analyte-genetic-variant'], name="loincTerm__supplementary_analyte_genetic_variant", curie=LOINC_PROPERTY.curie('analyte-genetic-variant'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_genetic_variant, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_chemical = Slot(uri=LOINC_PROPERTY['analyte-chemical'], name="loincTerm__supplementary_analyte_chemical", curie=LOINC_PROPERTY.curie('analyte-chemical'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_chemical, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_divisor_chemical = Slot(uri=LOINC_PROPERTY['analyte-divisor-chemical'], name="loincTerm__supplementary_analyte_divisor_chemical", curie=LOINC_PROPERTY.curie('analyte-divisor-chemical'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_divisor_chemical, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_clinical_drug = Slot(uri=LOINC_PROPERTY['analyte-clinical-drug'], name="loincTerm__supplementary_analyte_clinical_drug", curie=LOINC_PROPERTY.curie('analyte-clinical-drug'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_clinical_drug, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_system_core_anatomic_entity = Slot(uri=LOINC_PROPERTY['system-core-anatomic-entity'], name="loincTerm__supplementary_system_core_anatomic_entity", curie=LOINC_PROPERTY.curie('system-core-anatomic-entity'),
                   model_uri=LOINC.loincTerm__supplementary_system_core_anatomic_entity, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_organism = Slot(uri=LOINC_PROPERTY['analyte-organism'], name="loincTerm__supplementary_analyte_organism", curie=LOINC_PROPERTY.curie('analyte-organism'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_organism, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_challenge_route = Slot(uri=LOINC_PROPERTY['challenge-route'], name="loincTerm__supplementary_challenge_route", curie=LOINC_PROPERTY.curie('challenge-route'),
                   model_uri=LOINC.loincTerm__supplementary_challenge_route, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_analyte_allergen = Slot(uri=LOINC_PROPERTY['analyte-allergen'], name="loincTerm__supplementary_analyte_allergen", curie=LOINC_PROPERTY.curie('analyte-allergen'),
                   model_uri=LOINC.loincTerm__supplementary_analyte_allergen, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_class = Slot(uri=LOINC_PROPERTY.class_, name="loincTerm__supplementary_class", curie=LOINC_PROPERTY.curie('class_'),
                   model_uri=LOINC.loincTerm__supplementary_class, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_category = Slot(uri=LOINC_PROPERTY.category, name="loincTerm__supplementary_category", curie=LOINC_PROPERTY.curie('category'),
                   model_uri=LOINC.loincTerm__supplementary_category, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__supplementary_search = Slot(uri=LOINC_PROPERTY.category, name="loincTerm__supplementary_search", curie=LOINC_PROPERTY.curie('category'),
                   model_uri=LOINC.loincTerm__supplementary_search, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_anatomic_location_imaging_focus = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-imaging-focus'], name="loincTerm__primary_rad_anatomic_location_imaging_focus", curie=LOINC_PROPERTY.curie('rad-anatomic-location-imaging-focus'),
                   model_uri=LOINC.loincTerm__primary_rad_anatomic_location_imaging_focus, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_anatomic_location_laterality = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-laterality'], name="loincTerm__primary_rad_anatomic_location_laterality", curie=LOINC_PROPERTY.curie('rad-anatomic-location-laterality'),
                   model_uri=LOINC.loincTerm__primary_rad_anatomic_location_laterality, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_anatomic_location_laterality_presence = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-laterality-presence'], name="loincTerm__primary_rad_anatomic_location_laterality_presence", curie=LOINC_PROPERTY.curie('rad-anatomic-location-laterality-presence'),
                   model_uri=LOINC.loincTerm__primary_rad_anatomic_location_laterality_presence, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_anatomic_location_region_imaged = Slot(uri=LOINC_PROPERTY['rad-anatomic-location-region-imaged'], name="loincTerm__primary_rad_anatomic_location_region_imaged", curie=LOINC_PROPERTY.curie('rad-anatomic-location-region-imaged'),
                   model_uri=LOINC.loincTerm__primary_rad_anatomic_location_region_imaged, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_guidance_for_action = Slot(uri=LOINC_PROPERTY['rad-guidance-for-action'], name="loincTerm__primary_rad_guidance_for_action", curie=LOINC_PROPERTY.curie('rad-guidance-for-action'),
                   model_uri=LOINC.loincTerm__primary_rad_guidance_for_action, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_guidance_for_approach = Slot(uri=LOINC_PROPERTY['rad-guidance-for-approach'], name="loincTerm__primary_rad_guidance_for_approach", curie=LOINC_PROPERTY.curie('rad-guidance-for-approach'),
                   model_uri=LOINC.loincTerm__primary_rad_guidance_for_approach, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_guidance_for_object = Slot(uri=LOINC_PROPERTY['rad-guidance-for-object'], name="loincTerm__primary_rad_guidance_for_object", curie=LOINC_PROPERTY.curie('rad-guidance-for-object'),
                   model_uri=LOINC.loincTerm__primary_rad_guidance_for_object, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_guidance_for_presence = Slot(uri=LOINC_PROPERTY['rad-guidance-for-presence'], name="loincTerm__primary_rad_guidance_for_presence", curie=LOINC_PROPERTY.curie('rad-guidance-for-presence'),
                   model_uri=LOINC.loincTerm__primary_rad_guidance_for_presence, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_maneuver_maneuver_type = Slot(uri=LOINC_PROPERTY['rad-maneuver-maneuver-type'], name="loincTerm__primary_rad_maneuver_maneuver_type", curie=LOINC_PROPERTY.curie('rad-maneuver-maneuver-type'),
                   model_uri=LOINC.loincTerm__primary_rad_maneuver_maneuver_type, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_modality_subtype = Slot(uri=LOINC_PROPERTY['rad-modality-subtype'], name="loincTerm__primary_rad_modality_subtype", curie=LOINC_PROPERTY.curie('rad-modality-subtype'),
                   model_uri=LOINC.loincTerm__primary_rad_modality_subtype, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_modality_type = Slot(uri=LOINC_PROPERTY['rad-modality-type'], name="loincTerm__primary_rad_modality_type", curie=LOINC_PROPERTY.curie('rad-modality-type'),
                   model_uri=LOINC.loincTerm__primary_rad_modality_type, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_pharmaceutical_route = Slot(uri=LOINC_PROPERTY['rad-pharmaceutical-route'], name="loincTerm__primary_rad_pharmaceutical_route", curie=LOINC_PROPERTY.curie('rad-pharmaceutical-route'),
                   model_uri=LOINC.loincTerm__primary_rad_pharmaceutical_route, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_pharmaceutical_substance_given = Slot(uri=LOINC_PROPERTY['rad-pharmaceutical-substance-given'], name="loincTerm__primary_rad_pharmaceutical_substance_given", curie=LOINC_PROPERTY.curie('rad-pharmaceutical-substance-given'),
                   model_uri=LOINC.loincTerm__primary_rad_pharmaceutical_substance_given, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_reason_for_exam = Slot(uri=LOINC_PROPERTY['rad-reason-for-exam'], name="loincTerm__primary_rad_reason_for_exam", curie=LOINC_PROPERTY.curie('rad-reason-for-exam'),
                   model_uri=LOINC.loincTerm__primary_rad_reason_for_exam, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_subject = Slot(uri=LOINC_PROPERTY['rad-subject'], name="loincTerm__primary_rad_subject", curie=LOINC_PROPERTY.curie('rad-subject'),
                   model_uri=LOINC.loincTerm__primary_rad_subject, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_timing = Slot(uri=LOINC_PROPERTY['rad-timing'], name="loincTerm__primary_rad_timing", curie=LOINC_PROPERTY.curie('rad-timing'),
                   model_uri=LOINC.loincTerm__primary_rad_timing, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_view_aggregation = Slot(uri=LOINC_PROPERTY.rad_view_aggregation, name="loincTerm__primary_rad_view_aggregation", curie=LOINC_PROPERTY.curie('rad_view_aggregation'),
                   model_uri=LOINC.loincTerm__primary_rad_view_aggregation, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_rad_view_view_type = Slot(uri=LOINC_PROPERTY.rad_view_view_type, name="loincTerm__primary_rad_view_view_type", curie=LOINC_PROPERTY.curie('rad_view_view_type'),
                   model_uri=LOINC.loincTerm__primary_rad_view_view_type, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_document_kind = Slot(uri=LOINC_PROPERTY['document-kind'], name="loincTerm__primary_document_kind", curie=LOINC_PROPERTY.curie('document-kind'),
                   model_uri=LOINC.loincTerm__primary_document_kind, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_document_role = Slot(uri=LOINC_PROPERTY['document-role'], name="loincTerm__primary_document_role", curie=LOINC_PROPERTY.curie('document-role'),
                   model_uri=LOINC.loincTerm__primary_document_role, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_document_setting = Slot(uri=LOINC_PROPERTY['document-setting'], name="loincTerm__primary_document_setting", curie=LOINC_PROPERTY.curie('document-setting'),
                   model_uri=LOINC.loincTerm__primary_document_setting, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_document_subject_matter_domain = Slot(uri=LOINC_PROPERTY['document-subject-matter-domain'], name="loincTerm__primary_document_subject_matter_domain", curie=LOINC_PROPERTY.curie('document-subject-matter-domain'),
                   model_uri=LOINC.loincTerm__primary_document_subject_matter_domain, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincTerm__primary_document_type_of_service = Slot(uri=LOINC_PROPERTY['document-type-of-service'], name="loincTerm__primary_document_type_of_service", curie=LOINC_PROPERTY.curie('document-type-of-service'),
                   model_uri=LOINC.loincTerm__primary_document_type_of_service, domain=None, range=Optional[Union[str, LoincPartId]])

slots.loincPart__part_number = Slot(uri=LOINC.part_number, name="loincPart__part_number", curie=LOINC.curie('part_number'),
                   model_uri=LOINC.loincPart__part_number, domain=None, range=Optional[str])

slots.loincPart__part_type_name = Slot(uri=LOINC['part-type-name'], name="loincPart__part_type_name", curie=LOINC.curie('part-type-name'),
                   model_uri=LOINC.loincPart__part_type_name, domain=None, range=Optional[str])

slots.loincPart__part_name = Slot(uri=LOINC.part_name, name="loincPart__part_name", curie=LOINC.curie('part_name'),
                   model_uri=LOINC.loincPart__part_name, domain=None, range=Optional[str])

slots.loincPart__part_display_name = Slot(uri=LOINC.part_display_name, name="loincPart__part_display_name", curie=LOINC.curie('part_display_name'),
                   model_uri=LOINC.loincPart__part_display_name, domain=None, range=Optional[str])

slots.loincPart__part_status = Slot(uri=LOINC.status, name="loincPart__part_status", curie=LOINC.curie('status'),
                   model_uri=LOINC.loincPart__part_status, domain=None, range=Optional[str])
