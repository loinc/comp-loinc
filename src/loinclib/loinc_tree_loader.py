"""LOINC tree files loader."""

import logging
from enum import StrEnum

import pandas as pd
from pandas import DataFrame

from loinclib import LoinclibGraph
from loinclib.loinc_schema import LoincNodeType, LoincPartProps
from loinclib.loinc_tree_schema import (
    LoincDanglingNlpEdges,
    LoincTreeEdges,
    LoincTreeProps,
)


logger = logging.getLogger("LoincTreeLoader")


class LoincTreeSource(StrEnum):
    class_tree = "class.csv"
    component_tree = "component.csv"
    component_by_system_tree = "component_by_system.csv"
    document_tree = "document.csv"
    method_tree = "method.csv"
    panel_tree = "panel.csv"
    system_tree = "system.csv"
    nlp_tree = "nlp-matches.sssom.tsv"


class LoincTreeLoader:
    def __init__(self, config, graph: LoinclibGraph):
        self.config = config
        self.graph = graph

    def load_class_tree(self):
        self._load_tree(LoincTreeSource.class_tree)

    def load_component_tree(self):
        self._load_tree(LoincTreeSource.component_tree)

    def load_component_by_system_tree(self):
        self._load_tree(LoincTreeSource.component_by_system_tree)

    def load_document_tree(self):
        self._load_tree(LoincTreeSource.document_tree)

    def load_method_tree(self):
        self._load_tree(LoincTreeSource.method_tree)

    def load_panel_tree(self):
        self._load_tree(LoincTreeSource.panel_tree)

    def load_system_tree(self):
        self._load_tree(LoincTreeSource.system_tree)

    def load_all_trees(self):
        """Load all tree files"""
        self.load_class_tree()
        self.load_component_tree()
        self.load_component_by_system_tree()
        self.load_document_tree()
        self.load_method_tree()
        self.load_panel_tree()
        self.load_system_tree()
        self.load_nlp_tree()

    def _getsert_node(self, code: str, code_text: str):
        """Insert node if needed, else get, and return node."""
        node = self.graph.get_node_by_code(type_=LoincNodeType.LoincPart, code=code)
        if node is None:
            node = self.graph.getsert_node(type_=LoincNodeType.LoincPart, code=code, source="nlp")
            node.set_property(type_=LoincTreeProps.from_trees, value=False)
            node.set_property(type_=LoincPartProps.part_number, value=code)
            node.set_property(type_=LoincTreeProps.code_text, value=code_text)
        return node

    def load_nlp_tree(
        self,
        source: LoincTreeSource = LoincTreeSource.nlp_tree,
        default_similarity_threshold: float = 0.5,
    ):
        """Load tree data from our internal NLP matches SSSOM file to add dangling parts to the hierarchy."""
        # Read data
        if source in self.graph.loaded_sources:
            return
        try:
            df: pd.DataFrame = self.read_nlp_source(LoincTreeSource.nlp_tree).fillna("")
        except FileNotFoundError:
            logger.warning(
                f"File not found: {source}. Skipping NLP-based tree loading."
            )
            return

        # Formatting
        df["curator_approved"] = df["curator_approved"].apply(
            lambda x: (
                x
                if isinstance(x, bool)
                else (
                    True
                    if x.lower() == "true"
                    else False if x.lower() == "false" else ""
                )
            )
        )
        for col in ["subject_id", "object_id"]:
            df[col] = df[col].str.replace("https://loinc.org/", "")  # URI to code

        # Add to hierarchy
        similarity_threshold: float = self.config.config["loinc_nlp_tree"].get(
            "similarity_threshold", default_similarity_threshold
        )
        for tpl in df.itertuples():
            # @formatter:off
            (
                row_num,
                child_code,
                predicate_id,
                parent_code,
                child_code_text,
                parent_code_text,
                part_type_name,
                mapping_justification,
                confidence,
                subject_dangling_tf,
                object_dangling_tf,
                curator_approved_tf,
            ) = tpl
            # @formatter:on
            # if curator_approved is an invalid or null value, revert to confidence over threshold
            if curator_approved_tf == False or (
                curator_approved_tf != True and confidence < similarity_threshold
            ):
                continue
            child_node = self._getsert_node(child_code, child_code_text)
            parent_node = self._getsert_node(parent_code, parent_code_text)
            child_node.add_edge_single(
                type_=LoincDanglingNlpEdges.nlp_parent, to_node=parent_node
            )

        self.graph.loaded_sources[source] = {}

    def _load_tree(self, source: LoincTreeSource, from_nlp_source=False, multi_axial=False):
        if source in self.graph.loaded_sources:
            return

        dataframe = self.read_source(source)

        records_by_id = {}
        for tpl in dataframe.itertuples():
            # @formatter:off
            (
                row_num,
                id_,
                parent_id,
                level,
                code,
                sequence,
                code_text,
                component,
                property_,
                timing,
                system,
                scale,
                method,
            ) = tpl
            # @formatter:on

            records_by_id[id_] = (parent_id, code, code_text)

        for parent_id, code, code_text in records_by_id.values():
            if not code.startswith("LP"):
                continue

            part_node = self.graph.get_node_by_code(
                type_=LoincNodeType.LoincPart, code=code
            )
            if part_node is None:
                part_node = self.graph.getsert_node(
                    type_=LoincNodeType.LoincPart, code=code, source=f"tree.{source}"
                )
                part_node.set_property(type_=LoincTreeProps.from_trees, value=True)
                part_node.set_property(type_=LoincPartProps.part_number, value=code)
            part_node.set_property(type_=LoincTreeProps.code_text, value=code_text)

            part_node.set_property(type_=LoincPartProps.is_multiaxial, value=" | " in code_text)

            if parent_id:
                parent_node = self.graph.get_node_by_code(
                    type_=LoincNodeType.LoincPart, code=records_by_id[parent_id][1]
                )
                if parent_node is None:
                    parent_node = self.graph.getsert_node(
                        type_=LoincNodeType.LoincPart, code=records_by_id[parent_id][1], source=f"tree.{source}"
                    )
                    parent_node.set_property(
                        type_=LoincTreeProps.from_trees, value=True
                    )
                    parent_node.set_property(
                        type_=LoincPartProps.part_number,
                        value=records_by_id[parent_id][1],
                    )
                parent_node.set_property(
                    type_=LoincTreeProps.code_text, value=records_by_id[parent_id][2]
                )

                part_node.add_edge_single(
                    type_=LoincTreeEdges.tree_parent, to_node=parent_node
                )

        self.graph.loaded_sources[source] = {}

    def read_nlp_source(self, source: LoincTreeSource) -> DataFrame:
        path = self.config.get_curation_dir_path() / source.value
        df = pd.read_csv(path, sep="\t", comment="#").fillna("")
        # - filter non-match rows
        df = df[df["object_id"] != ""]
        return df

    def read_source(self, source: LoincTreeSource) -> DataFrame:
        path = self.config.get_loinc_trees_path() / source.value
        return pd.read_csv(path, dtype=str, na_filter=False)
