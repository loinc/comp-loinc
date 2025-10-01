import typing
from enum import StrEnum

import pandas as pd

from loinclib import LoinclibGraph, Node, Configuration, EdgeType, GeneralEdgeType
from loinclib.snomed_schema_v2 import SnomedNodeType, SnomedEdges, SnomedProperties


class SnomedSources(StrEnum):
    """Enum for the different sources of SNOMED data."""

    relations = "relations"
    descriptions = "descriptions"
    fully_specified_name = "fully_specified_name"


class SnomedLoader:
    """Class to load SNOMED data into a graph."""

    def __init__(self, *, graph: LoinclibGraph, config: Configuration):
        self.config = config
        self.graph = graph

    def read_relationship(self) -> pd.DataFrame:
        """Reads the SNOMED relationships file."""
        return pd.read_csv(
            self.config.get_snomed_relations_path(),
            dtype=str,
            na_filter=False,
            sep="\t",
        )

    def read_description(self) -> pd.DataFrame:
        """Reads the SNOMED descriptions."""
        return pd.read_csv(
            self.config.get_snomed_description_path(),
            dtype=str,
            na_filter=False,
            sep="\t",
        )

    def load_selected_relations(self, *types_: EdgeType) -> None:
        """Populates graph with node-(EDGE)->node's, for 1+ EDGEs (`*types_`)."""
        loaded_relationships = self.graph.loaded_sources.get(
            SnomedSources.relations, {}
        )

        # check if any relationship type is new
        new_relationships = False
        for type_ in types_:
            if type_ not in loaded_relationships:
                new_relationships = True

        if not new_relationships:
            return

        for tpl in self.read_relationship().itertuples():
            # @formatter:off
            (
                index,
                id_,
                effective_time,
                active,
                module_id,
                source_id,
                destination_id,
                # relationship_id,
                relationship_group,
                type_id,
                characteristic_type_id,
                modifier_id,
            ) = tpl
            # @formatter:on

            if active == "0":
                continue

            type_ = None
            try:
                type_ = self._get_snomed_edge_type(type_id)
            except ValueError:
                pass

            # check again if this specific relation type was already loaded
            if type_ in loaded_relationships:
                continue

            if type_ in types_:
                from_node: Node = self.graph.getsert_node(
                    type_=SnomedNodeType.Concept, code=source_id
                )
                from_node.set_property(
                    type_=SnomedProperties.concept_id, value=source_id
                )

                to_node: Node = self.graph.getsert_node(
                    type_=SnomedNodeType.Concept, code=destination_id
                )
                to_node.set_property(
                    type_=SnomedProperties.concept_id, value=destination_id
                )

                from_node.add_edge_single(type_, to_node=to_node)

                if type_ == SnomedEdges.is_a:
                  from_node.add_edge_single(GeneralEdgeType.has_parent, to_node=to_node, source="snomed")

        for type_ in types_:
            loaded_relationships[type_] = True


    def _get_snomed_edge_type(self, concept_id: str) -> typing.Optional[SnomedEdges]:
        for type_ in SnomedEdges:
            if type_.value.name == concept_id:
                return type_
        return None


    def load_fully_specified_names(self):
        """Populate SNOMED concept nodes in graph with their FSN (Fully Specified Names), and add any missing nodes in the process."""
        if SnomedSources.fully_specified_name in self.graph.loaded_sources:
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
                type_id,  # e.g., Fully Specified Name, Preferred Term, Synonym
                term,  # The term label
                case_significance_id,  # Whethe capitalization is important, and if so in what way.
            ) = tpl
            # @formatter:on

            if active == "0":
                continue

            term_type = None
            try:
                term_type = SnomedProperties(type_id)
            except ValueError:
                pass

            if term_type is not SnomedProperties.fully_specified_name:
                continue

            concept = self.graph.getsert_node(
                type_=SnomedNodeType.Concept, code=concept_id
            )
            concept.set_property(type_=SnomedProperties.concept_id, value=concept_id)
            concept.set_property(type_=term_type, value=term)

        self.graph.loaded_sources[SnomedSources.fully_specified_name] = {}
