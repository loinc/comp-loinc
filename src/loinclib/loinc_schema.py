from enum import StrEnum, Enum
from loinclib.schema_util import  get_enum_helper


class LoincNodeType(StrEnum):
    LoincTerm = "LoincTerm"
    LoincPart = "LoincPart"
    LoincClass = "LoincClass"


class LoincTermProps(StrEnum):
    loinc_number = "loinc_number"
    long_common_name = "long_common_name"
    short_name = "short_name"
    class_ = "class"
    class_type = "class_type"
    definition_description = "definition_description"
    status = "status"


# 14:38 $ csvtool col 8 LoincPartLink_Primary.csv | sort | uniq -c
# 101632 http://loinc.org/property/COMPONENT
# 3581 http://loinc.org/property/document-kind
# 1096 http://loinc.org/property/document-role
# 3584 http://loinc.org/property/document-setting
# 3006 http://loinc.org/property/document-subject-matter-domain
# 2453 http://loinc.org/property/document-type-of-service
# 55382 http://loinc.org/property/METHOD_TYP
# 101632 http://loinc.org/property/PROPERTY
# 6135 http://loinc.org/property/rad-anatomic-location-imaging-focus
# 4004 http://loinc.org/property/rad-anatomic-location-laterality
# 3986 http://loinc.org/property/rad-anatomic-location-laterality-presence
# 7064 http://loinc.org/property/rad-anatomic-location-region-imaged
# 1156 http://loinc.org/property/rad-guidance-for-action
#   349 http://loinc.org/property/rad-guidance-for-approach
#     476 http://loinc.org/property/rad-guidance-for-object
# 1028 http://loinc.org/property/rad-guidance-for-presence
#   444 http://loinc.org/property/rad-maneuver-maneuver-type
# 1181 http://loinc.org/property/rad-modality-subtype
# 6660 http://loinc.org/property/rad-modality-type
# 1949 http://loinc.org/property/rad-pharmaceutical-route
# 2446 http://loinc.org/property/rad-pharmaceutical-substance-given
# 471 http://loinc.org/property/rad-reason-for-exam
#   34 http://loinc.org/property/rad-subject
# 2770 http://loinc.org/property/rad-timing
# 3905 http://loinc.org/property/rad-view-aggregation
# 1991 http://loinc.org/property/rad-view-view-type
# 101632 http://loinc.org/property/SCALE_TYP
# 101632 http://loinc.org/property/SYSTEM
# 101632 http://loinc.org/property/TIME_ASPCT
# 1 Property

# https://stackoverflow.com/questions/74884921/how-to-add-attributes-to-a-enum-strenum
class LoincTermPrimaryEdges(StrEnum):
    def __new__(cls, value, order , prefix ):
        member = str.__new__(cls, value)
        member._value_ = value
        member.order = order
        member.prefix = prefix
        return member

    primary_component = "http://loinc.org/property/COMPONENT", 1, "C"
    primary_property = "http://loinc.org/property/PROPERTY", 2, "P"
    primary_time_aspect = "http://loinc.org/property/TIME_ASPCT", 3 , "TA"
    primary_system = "http://loinc.org/property/SYSTEM", 4, "S"
    primary_scale_type = "http://loinc.org/property/SCALE_TYP", 5, "ST"
    primary_method_type = "http://loinc.org/property/METHOD_TYP", 6 , "MT"

    # DOC
    primary_document_kind = "http://loinc.org/property/document-kind", 10, "DOC_K"
    primary_document_role = "http://loinc.org/property/document-role", 11 , "DOC_R"
    primary_document_setting = "http://loinc.org/property/document-setting", 12, "DOC_S"
    primary_document_subject_matter_domain = (
        "http://loinc.org/property/document-subject-matter-domain", 13, "DOC_SMD"
    )
    primary_document_type_of_service = (
        "http://loinc.org/property/document-type-of-service", 14, "DOC_TOS"
    )

    # Rad
    primary_rad_anatomic_location_imaging_focus = (
        "http://loinc.org/property/rad-anatomic-location-imaging-focus", 20, "RAD_ALIF"
    )
    primary_rad_anatomic_location_laterality = (
        "http://loinc.org/property/rad-anatomic-location-laterality", 21, "RAD_ALL"
    )
    primary_rad_anatomic_location_laterality_presence = (
        "http://loinc.org/property/rad-anatomic-location-laterality-presence", 22, "RAD_ALLP"
    )
    primary_rad_anatomic_location_region_imaged = (
        "http://loinc.org/property/rad-anatomic-location-region-imaged", 23, "RAD_ALRI"
    )
    primary_rad_guidance_for_action = (
        "http://loinc.org/property/rad-guidance-for-action", 24, "RAD_GFAc"
    )
    primary_rad_guidance_for_approach = (
        "http://loinc.org/property/rad-guidance-for-approach", 25, "RAD_GFAp"
    )
    primary_rad_guidance_for_object = (
        "http://loinc.org/property/rad-guidance-for-object", 26, "RAD_GFO"
    )
    primary_rad_guidance_for_presence = (
        "http://loinc.org/property/rad-guidance-for-presence", 27, "RAD_GFP"
    )
    primary_rad_maneuver_maneuver_type = (
        "http://loinc.org/property/rad-maneuver-maneuver-type", 28, "RAD_MMT"
    )
    primary_rad_modality_subtype = "http://loinc.org/property/rad-modality-subtype", 29, "RAD_MS"
    primary_rad_modality_type = "http://loinc.org/property/rad-modality-type", 30, "RAD_MT"
    primary_rad_pharmaceutical_route = (
        "http://loinc.org/property/rad-pharmaceutical-route", 31, "RAD_PR"
    )
    primary_rad_pharmaceutical_substance_given = (
        "http://loinc.org/property/rad-pharmaceutical-substance-given", 32, "RAD_PSG"
    )
    primary_rad_reason_for_exam = "http://loinc.org/property/rad-reason-for-exam", 33, "RAD_RFE"
    primary_rad_subject = "http://loinc.org/property/rad-subject", 34, "RAD_S"
    primary_rad_timing = "http://loinc.org/property/rad-timing", 35, "RAD_T"
    primary_rad_view_aggregation = "http://loinc.org/property/rad-view-aggregation", 36, "RAD_VA"
    primary_rad_view_view_type = "http://loinc.org/property/rad-view-view-type", 36, "RAD_VVT"

    def __repr__(self):
        return f"{self.order} -- {self.prefix} -- {self._name_} -- {self._value_}"

    @classmethod
    def get_enum(cls, string: str):
        return get_enum_helper(string, LoincTermPrimaryEdges)



# 14:38 $ csvtool col 8 LoincPartLink_Supplementary.csv | sort | uniq -c
# 204 http://loinc.org/property/adjustment
# 90944 http://loinc.org/property/analyte
# 101632 http://loinc.org/property/analyte-core
# 5723 http://loinc.org/property/analyte-divisor
# 25 http://loinc.org/property/analyte-divisor-suffix
# 1709 http://loinc.org/property/analyte-gene
# 425 http://loinc.org/property/analyte-numerator
# 24368 http://loinc.org/property/analyte-suffix
# 218515 http://loinc.org/property/category
# 6603 http://loinc.org/property/challenge
# 101632 http://loinc.org/property/CLASS
# 148 http://loinc.org/property/count
# 44709 http://loinc.org/property/METHOD_TYP
# 90944 http://loinc.org/property/PROPERTY
# 90944 http://loinc.org/property/SCALE_TYP
# 266570 http://loinc.org/property/search
# 22418 http://loinc.org/property/super-system
# 69832 http://loinc.org/property/system-core
# 90944 http://loinc.org/property/time-core
# 233 http://loinc.org/property/time-modifier
# 1 Property


class LoincTermSupplementaryEdges(StrEnum):
    def __new__(cls, value, order , prefix ):
        member = str.__new__(cls, value)
        member._value_ = value
        member.order = order
        member.prefix = prefix
        return member


    supplementary_adjustment = "http://loinc.org/property/adjustment", 100, "SUP_Ad"
    supplementary_analyte = "http://loinc.org/property/analyte", 101, "SUP_An"
    supplementary_analyte_core = "http://loinc.org/property/analyte-core", 102, "SUP_AC"
    supplementary_analyte_divisor = "http://loinc.org/property/analyte-divisor", 103, "SUP_AD"
    supplementary_analyte_divisor_suffix = (
        "http://loinc.org/property/analyte-divisor-suffix", 104, "SUP_ADS"
    )
    supplementary_analyte_gene = "http://loinc.org/property/analyte-gene", 105, "SUP_AG"
    supplementary_analyte_numerator = "http://loinc.org/property/analyte-numerator", 106, "SUP_AN"
    supplementary_analyte_suffix = "http://loinc.org/property/analyte-suffix", 107, "SUP_AS"
    supplementary_category = "http://loinc.org/property/category", 108, "SUP_Ca"
    supplementary_challenge = "http://loinc.org/property/challenge", 109, "SUP_Ch"
    supplementary_CLASS = "http://loinc.org/property/CLASS", 110, "SUP_Cl"
    supplementary_count = "http://loinc.org/property/count", 111, "SUP_C"
    supplementary_METHOD_TYP = "http://loinc.org/property/METHOD_TYP", 112, "SUP_MT"
    supplementary_PROPERTY = "http://loinc.org/property/PROPERTY", 113, "SUP_P"
    supplementary_SCALE_TYP = "http://loinc.org/property/SCALE_TYP", 114, "SUP_ST"
    supplementary_search = "http://loinc.org/property/search", 115, "SUP_S"
    supplementary_super_system = "http://loinc.org/property/super-system", 116, "SUP_SS"
    supplementary_system_core = "http://loinc.org/property/system-core", 117, "SUP_SC"
    supplementary_time_core = "http://loinc.org/property/time-core", 118, "SUP_TC"
    supplementary_time_modifier = "http://loinc.org/property/time-modifier", 119, "SUP_TM"

    def __repr__(self):
        return f"{self.order} -- {self.prefix} -- {self._name_} -- {self._value_}"

    @classmethod
    def get_enum(cls, string: str):
        return get_enum_helper(string, LoincTermSupplementaryEdges)


class LoincPartProps(StrEnum):
    part_number = "part_number"
    part_type_name = "part_type_name"
    part_name = "part_name"
    part_display_name = "part_display_name"
    status = "status"

    code_text__from_comp_hierarch = "part_text__from_comp_hierarch"
    code_text__from_tree = "code_text__from_tree"

    from_hierarchy = "from_hierarchy"


class LoincPartEdge(StrEnum):
    parent_comp_by_system = (
        "parent_comp_by_system"  # This edge comes from ComponentHierarchyBySystem.csv
    )


# loinc_schema: Schema = Schema()
#
# loinc_term = NodeType(type_=LoincNodeType.LoincTerm,
#                       schema=loinc_schema,
#                       base_url='https://loinc.org/',
#                       url_regex=r'^https?://loinc.org/(P<code>\d+-\d)$',
#                       curie_prefix='loinc',
#                       dynamic=False)
#
# loinc_schema.add_node_type(node_type=loinc_term)
#
# # properties
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.loinc_number))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.long_common_name))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.formal_name))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.short_name))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.class_))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincTermProps.class_type))
#
# # edges
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_component))
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_property))
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_time_aspect))
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_system))
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_scale_type))
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincTermEdges.primary_method_type))
#
#
# loinc_part = NodeType(type_=LoincNodeType.LoincPart,
#                       schema=loinc_schema,
#                       base_url='https://loinc.org/',
#                       url_regex=r'^https?://loinc.org/(P<code>LP\d+-\d)$',
#                       curie_prefix='loinc')
# loinc_schema.add_node_type(node_type=loinc_part)
#
# # properties
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincPartProps.part_number))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincPartProps.part_type_name))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincPartProps.part_name))
# loinc_term.add_property(PropertyType(node_type=loinc_term, type_key=LoincPartProps.part_display_name))
#
# # edge
# loinc_term.add_edge_type(EdgeType(node_type=loinc_term, type_=LoincPartEdges.sub_class_of))


class LoincClassProps(StrEnum):
    abbreviation = "Abbreviation"
    title = "title"
    part_number = "part_number"


class LoincClassEdge(StrEnum):
    part = "part"
