from dataclasses import dataclass

from loinclib import NodeType, EdgeType, PropertyType, NodeTypeArgs, PropertyTypeArgs, EdgeTypeArgs


@dataclass(kw_only=True)
class LoincNodeTypeArgs(NodeTypeArgs):
  pass


class LoincNodeType(NodeType):
  LoincTerm = LoincNodeTypeArgs(name="LoincTerm", id_prefix="loinc")
  LoincPart = LoincNodeTypeArgs(name="LoincPart", id_prefix="loinc")
  LoincClass = LoincNodeTypeArgs(name="LoincClass", id_prefix="loinc")


@dataclass(kw_only=True)
class LoincTermPropsArgs(PropertyTypeArgs):
  pass


class LoincTermProps(PropertyType):
  loinc_number = LoincTermPropsArgs(name="loinc_number")
  long_common_name = LoincTermPropsArgs(name="long_common_name")
  short_name = LoincTermPropsArgs(name="short_name")
  class_ = LoincTermPropsArgs(name="class")
  class_type = LoincTermPropsArgs(name="class_type")
  definition_description = LoincTermPropsArgs(name="definition_description")
  status = LoincTermPropsArgs(name="status")


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

@dataclass(kw_only=True)
class LoincTermPrimaryEdgesArgs(EdgeTypeArgs):
  pass

class LoincTermPrimaryEdges(EdgeType):

  primary_component = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/COMPONENT")
  primary_property = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/PROPERTY")
  primary_time_aspect = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/TIME_ASPCT")
  primary_system = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/SYSTEM")
  primary_scale_type = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/SCALE_TYP")
  primary_method_type = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/METHOD_TYP")

  primary_document_kind = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/document-kind")
  primary_document_role = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/document-role")
  primary_document_setting = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/document-setting")
  primary_document_subject_matter_domain = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/document-subject-matter-domain"
  )
  primary_document_type_of_service = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/document-type-of-service"
  )

  primary_rad_anatomic_location_imaging_focus = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-anatomic-location-imaging-focus"
  )
  primary_rad_anatomic_location_laterality = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-anatomic-location-laterality"
  )
  primary_rad_anatomic_location_laterality_presence = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-anatomic-location-laterality-presence"
  )
  primary_rad_anatomic_location_region_imaged = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-anatomic-location-region-imaged"
  )
  primary_rad_guidance_for_action = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-guidance-for-action"
  )
  primary_rad_guidance_for_approach = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-guidance-for-approach"
  )
  primary_rad_guidance_for_object = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-guidance-for-object"
  )
  primary_rad_guidance_for_presence = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-guidance-for-presence"
  )
  primary_rad_maneuver_maneuver_type = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-maneuver-maneuver-type"
  )
  primary_rad_modality_subtype = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-modality-subtype"
  )
  primary_rad_modality_type = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/rad-modality-type")
  primary_rad_pharmaceutical_route = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-pharmaceutical-route"
  )
  primary_rad_pharmaceutical_substance_given = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-pharmaceutical-substance-given"
  )
  primary_rad_reason_for_exam = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-reason-for-exam"
  )
  primary_rad_subject = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/rad-subject")
  primary_rad_timing = LoincTermPrimaryEdgesArgs(name="http://loinc.org/property/rad-timing")
  primary_rad_view_aggregation = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-view-aggregation"
  )
  primary_rad_view_view_type = LoincTermPrimaryEdgesArgs(
      name="http://loinc.org/property/rad-view-view-type"
  )

def get_by_name(cls, name: str) -> LoincTermPrimaryEdges:
  pass



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

@dataclass(kw_only=True)
class LoincTermSupplementaryEdgesArgs(EdgeTypeArgs):
  pass


class LoincTermSupplementaryEdges(EdgeType):
  supplementary_adjustment = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/adjustment")
  supplementary_analyte = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/analyte")
  supplementary_analyte_core = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/analyte-core")
  supplementary_analyte_divisor = LoincTermSupplementaryEdgesArgs(
      name="http://loinc.org/property/analyte-divisor"
  )
  supplementary_analyte_divisor_suffix = LoincTermSupplementaryEdgesArgs(
      name="http://loinc.org/property/analyte-divisor-suffix"
  )
  supplementary_analyte_gene = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/analyte-gene")
  supplementary_analyte_numerator = LoincTermSupplementaryEdgesArgs(
      name="http://loinc.org/property/analyte-numerator"
  )
  supplementary_analyte_suffix = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/analyte-suffix")
  supplementary_category = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/category")
  supplementary_challenge = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/challenge")
  supplementary_CLASS = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/CLASS")
  supplementary_count = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/count")
  supplementary_METHOD_TYP = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/METHOD_TYP")
  supplementary_PROPERTY = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/PROPERTY")
  supplementary_SCALE_TYP = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/SCALE_TYP")
  supplementary_search = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/search")
  supplementary_super_system = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/super-system")
  supplementary_system_core = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/system-core")
  supplementary_time_core = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/time-core")
  supplementary_time_modifier = LoincTermSupplementaryEdgesArgs(name="http://loinc.org/property/time-modifier")


@dataclass(kw_only=True)
class LoincPartPropsArgs(PropertyTypeArgs):
  pass


class LoincPartProps(PropertyType):
  part_number = LoincPartPropsArgs(name="part_number")
  part_type_name = LoincPartPropsArgs(name="part_type_name")
  part_name = LoincPartPropsArgs(name="part_name")
  part_display_name = LoincPartPropsArgs(name="part_display_name")
  status = LoincPartPropsArgs(name="status")

  code_text__from_comp_hierarch = LoincPartPropsArgs(name="part_text__from_comp_hierarch")
  code_text__from_tree = LoincPartPropsArgs(name="code_text__from_tree")

  from_hierarchy = LoincPartPropsArgs(name="from_hierarchy")

@dataclass(kw_only=True)
class LoincPartEdgeArgs(EdgeTypeArgs):
  pass

class LoincPartEdge(EdgeType):

  parent_comp_by_system = LoincPartEdgeArgs(
      name="parent_comp_by_system"  # This edge comes from ComponentHierarchyBySystem.csv
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

@dataclass(kw_only=True)
class LoincClassPropsArgs(PropertyTypeArgs):
  pass

class LoincClassProps(PropertyType):

  abbreviation = LoincClassPropsArgs(name="Abbreviation")
  title = LoincClassPropsArgs(name="title")
  part_number = LoincClassPropsArgs(name="part_number")

@dataclass(kw_only=True)
class LoincClassEdgesArgs(EdgeTypeArgs):
  pass

class LoincClassEdges(EdgeType):

  part = LoincClassEdgesArgs(name="part")
