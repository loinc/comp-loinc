import typing as t
from enum import StrEnum

import pandas as pd

import loinclib.loinc_schema as LS
from loinclib import GeneralEdgeType
from loinclib.config import Configuration
from loinclib.graph import Node, LoinclibGraph, GeneralProps
from loinclib.loinc_schema import LoincPartEdge, LoincPartProps, LoincClassEdges


class LoincElementSource(StrEnum):
  parts = "loinc.parts-file"
  primary_parts = "loinc.primary-parts"
  supplementary_parts = "loinc.supplementary-parts"
  component_by_system = "loinc.component-by-system"


class LoincSources(StrEnum):
  LoincTable__LoincCsv = "LoincTable/Loinc.csv"
  AccessoryFiles__PartFile__PartCsv = "AccessoryFiles/PartFile/Part.csv"
  AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv = (
    "AccessoryFiles/PartFile/LoincPartLink_Primary.csv"
  )
  AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv = (
    "AccessoryFiles/PartFile/LoincPartLink_Supplementary.csv"
  )
  AccessoryFiles__PartFile__PartRelatedCodeMappingCsv = (
    "AccessoryFiles/PartFile/PartRelatedCodeMapping.csv"
  )
  AccessoryFiles__ComponentHierarchyBySystem__ComponentHierarchyBySystemCsv = (
    "AccessoryFiles/ComponentHierarchyBySystem/ComponentHierarchyBySystem.csv"
  )
  AccessoryFiles__ComponentHierarchyBySystem__ComponentHierarchyBySystemCsv__part_parents = (
    "AccessoryFiles/ComponentHierarchyBySystem/ComponentHierarchyBySystem.csv"
  )
  Classes = "classes"


class LoincLoader:

  def __init__(self, *, graph: LoinclibGraph, configuration: Configuration):
    self.graph = graph
    self.configuration = configuration
    self.release_path = self.configuration.get_loinc_release_path()

  def load_loinc_table__loinc_csv(self) -> None:

    if LoincSources.LoincTable__LoincCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_loinc_table__loinc_csv().itertuples():
      (
        row_number,
        loinc_number,
        component,
        property_,
        time_aspect,
        system,
        scale_type,
        method_type,
        class_,
        version_last_changed,
        change_type,
        definition_description,
        status,
        consumer_name,
        class_type,
        formula,
        example_answers,
        survey_question_text,
        survey_question_source,
        units_required,
        related_names_2,
        short_name,
        order_obs,
        hl7_field_subfield_id,
        external_copyright_notice,
        example_units,
        long_common_name,
        example_ucum_units,
        status_reason,
        status_text,
        change_reason_public,
        common_test_rank,
        common_order_rank,
        hl7_attachement_structure,
        external_copyright_link,
        panel_type,
        ask_at_order_entry,
        associated_observations,
        version_first_released,
        valid_hl7_attachment_request,
        display_name,
      ) = tpl

      node: Node = self.graph.getsert_node(
          type_=LS.LoincNodeType.LoincTerm, code=loinc_number, source="loinc.loinc-csv"
      )

      # properties
      node.set_property(type_=LS.LoincTermProps.loinc_number, value=loinc_number)
      node.set_property(
          type_=LS.LoincTermProps.long_common_name, value=long_common_name
      )
      node.set_property(type_=LS.LoincTermProps.class_, value=class_)
      node.set_property(
          type_=LS.LoincTermProps.definition_description,
          value=definition_description,
      )
      node.set_property(type_=LS.LoincTermProps.class_type, value=class_type)
      node.set_property(type_=LS.LoincTermProps.status, value=status)
      node.set_property(type_=LS.LoincTermProps.short_name, value=short_name)
      node.set_property(type_=LS.LoincTermProps.display_name, value=display_name)
      if method_type:
        node.set_property(type_=LS.LoincTermProps.fully_specified_name,
                          value=f"{component}:{property_}:{time_aspect}:{system}:{scale_type}:{method_type}")
      else:
        node.set_property(type_=LS.LoincTermProps.fully_specified_name,
                          value=f"{component}:{property_}:{time_aspect}:{system}:{scale_type}:")

      # edges

    self.graph.loaded_sources[LoincSources.LoincTable__LoincCsv] = {}

  def load_accessory_files__part_file__part_csv(self) -> None:
    """Populates graph with part nodes & their most basic properties"""
    if LoincSources.AccessoryFiles__PartFile__PartCsv in self.graph.loaded_sources:
      return

    for tpl in self.read_accessory_files__part_file__part_csv().itertuples():
      (
        row_number,
        part_number,
        part_type_name,
        part_name,
        part_display_name,
        status,
      ) = tpl

      node: Node = self.graph.getsert_node(
          type_=LS.LoincNodeType.LoincPart, code=part_number, source=LoincElementSource.parts
      )
      node.set_property(type_=LS.LoincPartProps.part_number, value=part_number)
      node.set_property(
          type_=LS.LoincPartProps.part_type_name, value=part_type_name
      )
      node.set_property(type_=LS.LoincPartProps.part_name, value=part_name)
      node.set_property(type_=GeneralProps.label, value=part_name)
      node.set_property(
          type_=LS.LoincPartProps.part_display_name, value=part_display_name
      )
      node.set_property(type_=LS.LoincPartProps.status, value=status)
      node.set_property(type_=GeneralProps.code, value=part_number)

    self.graph.loaded_sources[LoincSources.AccessoryFiles__PartFile__PartCsv] = {}

  def __get_loinc_term_primary_edge_type(self, property_name: str) -> t.Optional[LS.LoincTermPrimaryEdges]:
    for edge in LS.LoincTermPrimaryEdges:
      if edge.value.name == property_name:
        return edge
    return None

  def load_accessory_files__part_file__loinc_part_link_primary_csv(self) -> None:
    """Populates graph part nodes with properties from the primary part model."""
    if (
        LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv
        in self.graph.loaded_sources
    ):
      return

    for (
        tpl
    ) in (
        self.read_accessory_files__part_file__loinc_part_link_primary_csv().itertuples()
    ):
      (
        row_number,
        loinc_number,
        long_common_name,
        part_number,
        part_name,
        part_code_system,
        part_type_name,
        link_type_name,
        property_,
      ) = tpl

      loinc_node: Node = self.graph.getsert_node(
          LS.LoincNodeType.LoincTerm, loinc_number, source=LoincElementSource.primary_parts
      )
      loinc_node.set_property(
          type_=LS.LoincTermProps.loinc_number, value=loinc_number
      )

      part_node: Node = self.graph.getsert_node(
          LS.LoincNodeType.LoincPart, part_number, source=LoincElementSource.primary_parts
      )
      part_node.set_property(type_=LoincPartProps.part_number, value=part_number)

      loinc_node.add_edge_single(
          self.__get_loinc_term_primary_edge_type(property_), part_node, False
      )

    self.graph.loaded_sources[
      LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv
    ] = {}

  def __get_loinc_term_supplimentary_edge_type(self, property_name: str) -> t.Optional[LS.LoincTermSupplementaryEdges]:
    for edge in LS.LoincTermSupplementaryEdges:
      if edge.value.name == property_name:
        return edge
    return None

  def load_accessory_files__part_file__loinc_part_link_supplementary_csv(
      self,
  ) -> None:
    """Populates graph part nodes with properties from the supplementary part model."""
    if (
        LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv
        in self.graph.loaded_sources
    ):
      return

    for (
        tpl
    ) in (
        self.read_accessory_files__part_file__loinc_part_link_supplementary_csv().itertuples()
    ):
      (
        row_number,
        loinc_number,
        long_common_name,
        part_number,
        part_name,
        part_code_system,
        part_type_name,
        link_type_name,
        property_,
      ) = tpl

      loinc_node: Node = self.graph.getsert_node(
          LS.LoincNodeType.LoincTerm, loinc_number, source=LoincElementSource.supplementary_parts
      )
      loinc_node.set_property(
          type_=LS.LoincTermProps.loinc_number, value=loinc_number
      )

      part_node: Node = self.graph.getsert_node(
          LS.LoincNodeType.LoincPart, part_number, source=LoincElementSource.supplementary_parts
      )
      part_node.set_property(
          type_=LS.LoincPartProps.part_number, value=part_number
      )

      loinc_node.add_edge_single(
          self.__get_loinc_term_supplimentary_edge_type(property_),
          part_node
      )

    self.graph.loaded_sources[
      LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv
    ] = {}

  def load_part_parents_from_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv(
      self,
  ):
    # raise UnsupportedOperation()
    if (
        LoincSources.AccessoryFiles__ComponentHierarchyBySystem__ComponentHierarchyBySystemCsv__part_parents
        in self.graph.loaded_sources
    ):
      return

    for (
        tpl
    ) in (
        self.read_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv().itertuples()
    ):

      (row_number, path_to_root, sequence, immediate_parent, code, code_text) = (
        tpl
      )

      if not code.startswith("LP"):
        continue

      part_node: Node = self.graph.get_node_by_code(
          type_=LS.LoincNodeType.LoincPart, code=code
      )
      if part_node is None:
        part_node = self.graph.getsert_node(LS.LoincNodeType.LoincPart, code,
                                            source=LoincElementSource.component_by_system)
        part_node.set_property(type_=LoincPartProps.part_number, value=code)

      sources = part_node.get_property(GeneralProps.sources)
      if sources is None:
        sources = set()
        part_node.set_property(type_=GeneralProps.sources, value=sources)
      sources.add(LoincElementSource.component_by_system)

      part_node.set_property(type_=LoincPartProps.from_hierarchy, value=True)  # todo: remove due to sources approach

      part_node.set_property(
          type_=LS.LoincPartProps.code_text__from_comp_hierarch, value=code_text
      )

      part_node.set_property(type_=LoincPartProps.is_multiaxial, value=" | " in code_text)

      if immediate_parent:
        parent_node: Node = self.graph.get_node_by_code(
            type_=LS.LoincNodeType.LoincPart, code=immediate_parent
        )
        if parent_node is None:
          parent_node = self.graph.getsert_node(
              LS.LoincNodeType.LoincPart, immediate_parent, source=LoincElementSource.component_by_system
          )
          parent_node.set_property(
              type_=LoincPartProps.part_number, value=immediate_parent
          )
        parent_node.set_property(
            type_=LoincPartProps.from_hierarchy, value=True
        )

        part_node.add_edge_single(
            type_=LoincPartEdge.parent_comp_by_system, to_node=parent_node,
            source=LoincElementSource.component_by_system
        )
        part_node.add_edge_single(
            type_=GeneralEdgeType.has_parent, to_node=parent_node, source=LoincElementSource.component_by_system
        )

    self.graph.loaded_sources[
      LoincSources.AccessoryFiles__ComponentHierarchyBySystem__ComponentHierarchyBySystemCsv__part_parents
    ] = {}

  def load_loinc_classes(self):
    if LoincSources.Classes in self.graph.loaded_sources:
      return

    for tpl in self.read_loinc_classes_csv().itertuples():
      (row_number, abbreviation, title, part_number) = tpl

      class_node = self.graph.getsert_node(
          type_=LS.LoincNodeType.LoincClass, code=abbreviation
      )
      class_node.set_property(
          type_=LS.LoincClassProps.abbreviation, value=abbreviation
      )
      class_node.set_property(type_=LS.LoincClassProps.title, value=title)
      class_node.set_property(
          type_=LS.LoincClassProps.part_number, value=part_number
      )

      part_node = self.graph.getsert_node(
          type_=LS.LoincNodeType.LoincPart, code=part_number
      )

      class_node.add_edge_single(type_=LoincClassEdges.part, to_node=part_node)

    self.graph.loaded_sources[LoincSources.Classes] = {}

  def read_loinc_table__loinc_csv(self) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path / LoincSources.LoincTable__LoincCsv,
        dtype=str,
        na_filter=False,
    )

  def read_accessory_files__part_file__part_csv(self) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path / LoincSources.AccessoryFiles__PartFile__PartCsv,
        dtype=str,
        na_filter=False,
    )

  def read_accessory_files__part_file__loinc_part_link_primary_csv(
      self,
  ) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path
        / LoincSources.AccessoryFiles__PartFile__LoincPartLink_PrimaryCsv,
        dtype=str,
        na_filter=False,
    )

  def read_accessory_files__part_file__loinc_part_link_supplementary_csv(
      self,
  ) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path
        / LoincSources.AccessoryFiles__PartFile__LoincPartLink_SupplementaryCsv,
        dtype=str,
        na_filter=False,
    )

  def read_accessory_files__part_file__part_related_code_mapping_csv(
      self,
  ) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path
        / LoincSources.AccessoryFiles__PartFile__PartRelatedCodeMappingCsv,
        dtype=str,
        na_filter=False,
    )

  def read_accessory_files__component_hierarchy_by_system__component_hierarchy_by_system_csv(
      self,
  ) -> pd.DataFrame:
    return pd.read_csv(
        self.release_path
        / LoincSources.AccessoryFiles__ComponentHierarchyBySystem__ComponentHierarchyBySystemCsv,
        dtype=str,
        na_filter=False,
    )

  def read_loinc_classes_csv(self) -> pd.DataFrame:
    return pd.read_csv(
        self.configuration.get_loinc_classes_path(), dtype=str, na_filter=False
    )
