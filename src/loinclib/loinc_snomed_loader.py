from enum import StrEnum

import pandas as pd

from loinclib import LoinclibGraph, SnomedNodeType, SnomedEdges, Configuration, GeneralEdgeType, GeneralProps
from loinclib.loinc_schema import LoincNodeType, LoincPartProps
from loinclib.loinc_snomed_schema import LoincSnomedEdges
from loinclib.snomed_schema_v2 import SnomedProperties


class LoincSnomedSources(StrEnum):
  description = "description"
  identifier = "identifier"
  relation = "relation"
  part_mapping = "part_mapping"


class LoincSnomedLoader:
  def __init__(self, config, graph: LoinclibGraph):
    self.config: Configuration = config
    self.graph = graph

  def load_identifier(self):
    if LoincSnomedSources.identifier in self.graph.loaded_sources:
      return

    for tpl in self.read_identifiers().itertuples():
      (
        index,
        alternate_identifier,  # loinc term code
        effective_time,
        active,
        module_id,
        identifier_schema_id,  # loinc
        referenced_component_id,
      ) = tpl

      loinc_node = self.graph.getsert_node(
          type_=LoincNodeType.LoincTerm, code=alternate_identifier
      )
      snomed_node = self.graph.getsert_node(
          type_=SnomedNodeType.Concept, code=referenced_component_id
      )

      loinc_node.add_edge_single(type_=LoincSnomedEdges.loinc_term_maps_to, to_node=snomed_node)
      loinc_node.add_edge_single(type_=GeneralEdgeType.mapped_to, to_node=snomed_node)

    self.graph.loaded_sources[LoincSnomedSources.identifier] = {}

  def load_description(self):
    if LoincSnomedSources.description in self.graph.loaded_sources:
      return

    for tpl in self.read_description().itertuples():
      (
        index,
        id_,
        effective_time,
        active,
        module_id,
        concept_id,
        language_code,
        type_id,
        term,
        case_significance_id,
      ) = tpl

      snomed_node = self.graph.getsert_node(SnomedNodeType.Concept, concept_id)
      type_ = SnomedProperties(type_id)
      snomed_node.set_property(
          type_=type_, value=term
      )
      snomed_node.set_property(
          type_=SnomedProperties.concept_id, value=concept_id
      )

    self.graph.loaded_sources[LoincSnomedSources.description] = {}

  def load_relationship(self):
    if LoincSnomedSources.relation in self.graph.loaded_sources:
      return

    for tpl in self.read_relationship().itertuples():
      (
        index,
        id_,
        effective_time,
        active,
        module_id,
        source_id,
        destination_id,
        relationship_group,
        type_id,
        characteristic_type_id,
        modifier_id,
      ) = tpl

      from_node = self.graph.getsert_node(
          type_=SnomedNodeType.Concept, code=source_id
      )
      to_node = self.graph.getsert_node(
          type_=SnomedNodeType.Concept, code=destination_id
      )
      type_ = SnomedEdges(type_id)
      from_node.add_edge_single(type_=type_, to_node=to_node)

    self.graph.loaded_sources[LoincSnomedSources.relation] = {}

  def load_part_mapping(self):
    """Populate graph with SNOMED<->LOINC part mappings from SNOMED(-LOINC) Ontology."""
    if LoincSnomedSources.part_mapping in self.graph.loaded_sources:
      return

    for tpl in self.read_part_mapping().itertuples():

      (
        index,
        source_code,
        source_display,
        status,
        part_type_name,
        target_code,
        target_display,
        relationship_type_code,
        relationship_type_display,
        no_map_flag,
        status,
      ) = tpl

      if target_code:
        loinc_part_node = self.graph.getsert_node(
            type_=LoincNodeType.LoincPart, code=source_code, source="snomed-mappings"
        )
        loinc_part_node.set_property(
            type_=LoincPartProps.part_number, value=source_code
        )
        loinc_part_node.set_property(
            type_=GeneralProps.code, value=source_code
        )

        snomed_cocept = self.graph.getsert_node(
            type_=SnomedNodeType.Concept, code=target_code, source="snomed-mappings"
        )
        snomed_cocept.set_property(
            type_=SnomedProperties.concept_id, value=target_code
        )
        snomed_cocept.set_property(
            type_=GeneralProps.code, value=target_code
        )
        snomed_cocept.set_property(
            type_=SnomedProperties.ID_900000000000003001, value=target_display
        )

        loinc_part_node.add_edge_single(
            type_=GeneralEdgeType.mapped_to, to_node=snomed_cocept, source="snomed-mappings"
        )

    self.graph.loaded_sources[LoincSnomedSources.part_mapping] = {}

  def map_loinc_part_to_snomed_concept(self):

    for loinc in self.graph.get_nodes(LoincNodeType.LoincTerm):
      for snomed_node in loinc.get_out_nodes(edge_types=[LoincSnomedEdges.loinc_term_maps_to],
                                             node_types=[SnomedNodeType.Concept]):
        pass

    pass

  def read_description(self):
    return pd.read_csv(
        self.config.get_loinc_snomed_description_path(),
        dtype=str,
        na_filter=False,
        sep="\t",
    )

  def read_identifiers(self):
    return pd.read_csv(
        self.config.get_loinc_snomed_identifier_path(),
        dtype=str,
        na_filter=False,
        sep="\t",
    )

  def read_relationship(self):
    return pd.read_csv(
        self.config.get_loinc_snomed_relationship_path(),
        dtype=str,
        na_filter=False,
        sep="\t",
    )

  def read_part_mapping(self):
    return pd.read_csv(
        self.config.get_loinc_snomed_part_mapping_path(),
        dtype=str,
        na_filter=False,
        sep="\t",
    )
