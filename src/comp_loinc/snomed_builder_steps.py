"""SNOMED Builder: Populate module with entity objects"""

import logging
import typing as t

from comp_loinc import Runtime
from comp_loinc.config import FAST_RUN_N_PARTS
from comp_loinc.datamodel import SnomedConcept
from loinclib import (
  Configuration,
  SnomedNodeType,
  LoincNodeType,
  SnomedEdges,
  SnomedLoader, GeneralEdgeType,
)
from loinclib.loinc_snomed_loader import LoincSnomedLoader
from loinclib.snomed_schema_v2 import SnomedProperties


class SnomedBuilderSteps:
    """SNOMED Builder Steps"""

    def __init__(self, *, configuration: Configuration):
        self.configuration = configuration
        self.runtime: t.Optional[Runtime] = None
        self.logger = logging.getLogger(self.__class__.__name__)

    def setup_cli_builder_steps_all(self, builder):
        """Connects builder CLI commands to their methods that execute said commands."""
        builder.cli.command(
            "sct-loinc-part-map-instances",
            help="Add SNOMED entities for the LOINC part mappings",
        )(self.loinc_part_mapping_instances)

        builder.cli.command(
            "sct-close-isa", help="Ancestor is-a closure on concepts in current module."
        )(self.close_is_a)

        builder.cli.command("sct-label", help="Apply label to existing concepts.")(
            self.label
        )

        builder.cli.command(
            "sct-check-cycles", help="Apply label to existing concepts."
        )(self.check_cycles)

    def loinc_part_mapping_instances(self):
        """Generates any missing LinkML SnomedConcept entities for any that are mapped to LOINC parts."""
        loader = LoincSnomedLoader(config=self.configuration, graph=self.runtime.graph)
        loader.load_part_mapping()

        count = 0
        for part in self.runtime.graph.get_nodes(type_=LoincNodeType.LoincPart):
            count = count + 1
            if self.configuration.fast_run and count > FAST_RUN_N_PARTS:
                break
            for edge in part.get_all_out_edges():

                if edge.to_node.get_node_type() == SnomedNodeType.Concept:
                    concept: SnomedConcept = self.runtime.current_module.get_entity(
                        entity_id=edge.to_node.node_id, entity_class=SnomedConcept
                    )
                    if concept is None:
                        concept = SnomedConcept(id=edge.to_node.node_id)
                        concept.fully_specified_name = edge.to_node.get_property(
                            type_=SnomedProperties.fully_specified_name
                        )
                        self.runtime.current_module.add_entity(concept)

    def close_is_a(self):
        """Populates LinkML entities with is-a relationships."""
        loader = SnomedLoader(config=self.configuration, graph=self.runtime.graph)
        loader.load_selected_relations(SnomedEdges.is_a.value.name)

        seen_set = set()
        current_set = set()
        todo_set = set()

        for concept in self.runtime.current_module.get_entities_of_type(
            entity_class=SnomedConcept
        ):
            current_set.add(concept.id)

        while len(current_set) > 0:
            for child_id in current_set:
                child_node = self.runtime.graph.get_node_by_id(
                    node_id=child_id
                )

                for edge in child_node.get_all_out_edges():

                    if edge.handler.type_ is SnomedEdges.is_a:
                        parent_node = edge.to_node
                        parent_id = parent_node.get_property(
                            type_=SnomedProperties.concept_id
                        )

                        if parent_id not in seen_set and parent_id not in current_set:
                            todo_set.add(parent_id)

                        child = self.runtime.current_module.get_entity(
                            entity_id=child_id, entity_class=SnomedConcept
                        )
                        if child is None:
                            child = SnomedConcept(id=child_id)
                            self.runtime.current_module.add_entity(child)

                        parent = self.runtime.current_module.get_entity(
                            entity_id=parent_id, entity_class=SnomedConcept
                        )
                        if parent is None:
                            parent = SnomedConcept(id=parent_id)
                            self.runtime.current_module.add_entity(parent)

                        child.sub_class_of.append(parent)

            seen_set = seen_set.union(current_set)
            current_set = todo_set
            todo_set = set()

    def check_cycles(self):
        for concept in self.runtime.current_module.get_entities_of_type(
            entity_class=SnomedConcept
        ):
            path: t.List[str] = [concept.id]
            self._check_cycle(concept, path)

    def _check_cycle(self, concept: SnomedConcept, path: t.List[str]):
        parent: SnomedConcept
        for parent in concept.sub_class_of:
            if parent.id in path:
                self.logger.warning(
                    f"Cycle: from {path[0]} to path: {parent.id} with paths: {path}"
                )
            else:
                path.append(parent.id)
                self._check_cycle(parent, path)
                path.pop()

    def label(self):
        """Updates SnomedConcepts with their fully specified names as labels."""
        loader = SnomedLoader(config=self.configuration, graph=self.runtime.graph)
        loader.load_fully_specified_names()

        concept: SnomedConcept
        for concept in self.runtime.current_module.get_entities_of_type(
            entity_class=SnomedConcept
        ):
            concept_node = self.runtime.graph.get_node_by_id(
               node_id=concept.id
            )
            fsn = concept_node.get_property(type_=SnomedProperties.fully_specified_name)
            if fsn is None:
                # just in case we have a fsn from the LOINC mappings
                concept.entity_label = f"SCT   {concept.fully_specified_name}"
            else:
                concept.entity_label = f"SCT   {fsn}"
