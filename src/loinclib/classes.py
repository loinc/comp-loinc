from __future__ import annotations

import typing as t
from pathlib import Path

import networkx as nx
import pandas as pd

import loinclib as ll


class LoincRelease:

    def __init__(self, release_path: Path, loinc_version: str, trees_path: Path):
        self.release_path: Path = release_path
        self.trees_path: Path = trees_path
        self.loinc_version: str = loinc_version
        self.graph: nx.MultiDiGraph = nx.MultiDiGraph()

        self.__parsed_parts = False

        self.__parsed_class_tree = False
        self.__parsed_component_tree = False
        self.__parsed_component_by_system_tree = False
        self.__parsed_document_tree = False
        self.__parsed_method_tree = False
        self.__parsed_system_tree = False

        self.__parsed_loincs = False

    #######################
    #
    #######################

    def node_ids_for_type(self, node_type: t.Any) -> t.List[str]:
        node_ids = [n for n in self.graph.nodes if
                    node_type.is_type(n)]
        return node_ids

    def node_properties(self, node_id: str) -> dict:
        return self.graph.nodes[node_id]

    def out_node_ids(self, from_node_id: str, edge_type: t.Any):
        edges = self.graph.out_edges(nbunch=from_node_id, keys=True,
                                     data=ll.AttributeKey.graph_entity_type)

        result = {edge_key: to_id for (from_id, to_id, edge_key, value) in edges if value == edge_type}
        return result

    def in_node_ids(self, to_node_id: str, edge_type: t.Any):
        edges = self.graph.in_edges(nbunch=to_node_id, keys=True,
                                    data=ll.AttributeKey.graph_entity_type)

        result_map = dict()
        for from_id, to_id, edge_key, value in edges:
            if value == edge_type:
                result_map[f'{from_id}-{edge_key}'] = from_id

            pass
        result = {edge_key: from_id for (from_id, to_id, edge_key, value) in edges if value == edge_type}
        return result_map

    def add_node_attribute(self,
                           *,
                           node_id: str,
                           attribute_name: t.Hashable,
                           attribute_value: t.Any,
                           create_node: bool = True,
                           single_value: bool = True,
                           ignore_empty: bool = True,
                           ):
        if not node_id:
            raise ValueError(f'Invalid node id: {node_id}')
        # Ignore empty
        if not attribute_value and isinstance(attribute_value, str) and ignore_empty:
            return

        if node_id not in self.graph:
            if create_node:
                self.graph.add_node(node_id)
            else:
                raise ValueError(
                    f'Node {node_id} not in graph, while attempting to add attribute: {attribute_name} and value: {attribute_value}')
        node = self.graph.nodes.get(node_id, None)
        if attribute_name in node:
            if single_value:
                current_value = node[attribute_name][0]
                if attribute_value == current_value:
                    # No error is the value is the same
                    return
                else:
                    raise ValueError(
                        f'Node: {node_id} already has attribute: "{attribute_name}" and value: '
                        f'"{node[attribute_name]}" while setting '
                        f'new AND different value: "{attribute_value}" and in single value mode.')
            self.graph.nodes[node_id][attribute_name].append(attribute_value)
        else:
            self.graph.nodes[node_id][attribute_name] = [attribute_value]

    def add_edge_type(self, from_node_id: str, to_node_id: str, edge_type: ll.EdgeType, multiple: bool = False):

        if not from_node_id or not to_node_id:
            raise ValueError(f'From node: {from_node_id} or to node: {to_node_id} is falsy.')

        out_nodes = self.out_node_ids(from_node_id, edge_type)
        if out_nodes and not multiple:
            return

        key = self.graph.add_edge(from_node_id, to_node_id)
        self.graph.edges[from_node_id, to_node_id, key][ll.AttributeKey.graph_entity_type] = edge_type

    #######################
    # Loinc related parsing
    #######################

    def parse_LoincTable_Loinc_csv(self) -> None:
        if self.__parsed_loincs:
            return

        for tpl in self.read_LoincTable_Loinc_csv().itertuples():
            (row_number,
             loinc_number,
             component,
             _property,
             time_aspect,
             system,
             scale_type,
             method_type,
             _class,
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
             common_si_test_rank,
             hl7_attachement_structure,
             external_copyright_link,
             panel_type,
             ask_at_order_entry,
             associated_observations,
             version_first_released,
             valid_hl7_attachement_request,
             display_name
             ) = tpl

            # node_id = NodePrefix.loinc_code + loinc_number
            node_id = ll.NodeType.loinc_code.node_id_of_identifier(loinc_number)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.code,
                                    attribute_value=loinc_number,
                                    single_value=True)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_long_common_name,
                                    attribute_value=long_common_name,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_short_name,
                                    attribute_value=short_name)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_short_name,
                                    attribute_value=short_name)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_definition,
                                    attribute_value=definition_description)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_component,
                                    attribute_value=component,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_property,
                                    attribute_value=_property,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_time_aspect,
                                    attribute_value=time_aspect,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_system,
                                    attribute_value=system,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_scale_type,
                                    attribute_value=scale_type,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_method_type,
                                    attribute_value=method_type,
                                    single_value=True)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_class,
                                    attribute_value=_class,
                                    single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_class_type,
                                    attribute_value=class_type,
                                    single_value=True)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.status,
                                    attribute_value=status)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_version_first_released,
                                    attribute_value=version_first_released, single_value=True)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.loinc_version_last_changed,
                                    attribute_value=version_last_changed, single_value=True)

        self.__parsed_loincs = True

    #######################
    # Part related parsing
    #######################

    def parse_AccessoryFiles_PartFile_Part_csv(self) -> None:

        if self.__parsed_parts:
            return

        for tpl in self.read_AccessoryFiles_PartFile_Part_csv().itertuples():
            (row_number, code, part_type, part_name, part_display, status) = tpl

            node_id = ll.NodeType.loinc_part.node_id_of_identifier(code)

            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.code,
                                    attribute_value=code)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.part_type,
                                    attribute_value=part_type)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.part_name,
                                    attribute_value=part_name)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.part_display_name,
                                    attribute_value=part_display)
            self.add_node_attribute(node_id=node_id, attribute_name=ll.NodeAttributeKey.status,
                                    attribute_value=status)

        self.__parsed_parts = True

    def parse_AccessoryFiles_PartFile_LoincPartLink_Primary_csv(self) -> None:
        for tpl in self.read_AccessoryFiles_PartFile_LoincPartLink_Primary_csv().itertuples():
            (row_number,
             loinc_number,
             long_common_name,
             part_number,
             part_name,
             part_code_system,
             part_type_name,
             link_type_name,
             property_uri) = tpl

            from_loinc_id = ll.NodeType.loinc_code.node_id_of_identifier(loinc_number)
            to_loinc_id = ll.NodeType.loinc_part.node_id_of_identifier(part_number)
            rel_type = ll.LoincPrimaryEdgeType.type_of(property_uri)
            self.add_edge_type(from_loinc_id, to_loinc_id, rel_type)

    def parse_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv(self) -> None:
        raise NotImplemented()
        for tpl in self.read_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv().itertuples():
            (row_number, loinc_number, long_common_name, part_number, part_name,
             part_code_system, part_type_name, link_type_name, property_uri) = tpl

    def parse_AccessoryFiles_ComponentHierarchyBySystem_ComponentHierarchyBySystem_csv(self):
        pass

        # for tpl in self.read_AccessoryFiles_ComponentHierarchyBySystem_ComponentHierarchyBySystem_csv().itertuples():
        #     (row_number, path, sequence, immediate_parent, code, code_text) = tpl
        #
        #     parent = self.entity_map_by_code.setdefault(immediate_parent, LoincEntity(immediate_parent)) \
        #         if immediate_parent else None
        #     child = self.entity_map_by_code.setdefault(code, LoincEntity(code))
        #     child.display = code_text
        #
        #     if parent:
        #         parent.children.add(child)
        #         child.parents.add(parent)

    def parse_all_trees(self):
        self.parse_tree_class()
        self.parse_tree_component()
        self.parse_tree_component_by_system()
        self.parse_tree_document_ontology()
        self.parse_tree_method()
        self.parse_tree_system()


    def parse_tree_class(self):
        if self.__parsed_class_tree:
            return
        self._parse_tree('class')
        self.__parsed_class_tree = True

    def parse_tree_component(self):
        if self.__parsed_component_tree:
            return
        self._parse_tree('component')
        self.__parsed_component_tree = True

    def parse_tree_component_by_system(self):
        if self.__parsed_component_by_system_tree:
            return
        self._parse_tree('component_by_system')
        self.__parsed_component_by_system_tree = True

    def parse_tree_document_ontology(self):
        if self.__parsed_document_tree:
            return
        self._parse_tree('document_ontology')
        self.__parsed_document_tree = True

    def parse_tree_method(self):
        if self.__parsed_method_tree:
            return
        self._parse_tree('method')
        self.__parsed_method_tree = True

    def parse_tree_system(self):
        if self.__parsed_system_tree:
            return
        self._parse_tree('system')
        self.__parsed_system_tree = True

    def _parse_tree(self, tree_name: str):

        # Columns:
        # Id,ParentId,Code,Sequence,CodeText,Component,Property,Timing,System,Scale,Method
        #  - Id - integer id value of the current record
        #  - ParentId - integer id value of the current record's parent Id field
        #  - Level - integer value indicating the node's level in the tree (e.g., a node with a level of 5 will have 5
        #       parent nodes)
        #  - Code - the LOINC Part or LOINC term whose hierarchy path is being described in a given row
        #  - Sequence - the order in which the LOINC Part or term in this row (specified in the Code column) appears
        #       under its immediate parent (i.e., the Part with the matching Id value in the ParentId column)
        #  - CodeText - the name of the LOINC Part or the Long Common Name of the LOINC term depending on the concept in
        #       the Code column
        #  - Component - the component value of the term if the Code is a LOINC term
        #  - Property - the property value of the term if the Code is a LOINC term
        #  - Timing - the timing value of the term if the Code is a LOINC term
        #  - NOTE: in documentaiton. System - ....
        #  - Scale - the scale value of the term if the Code is a LOINC term
        #  - Method - the method value of the term if the Code is a LOINC term

        id_to_code = {}

        frame = self._read_tree(tree_name)

        # We need this map of entry id to codes to be able to look up related codes.
        for tpl in frame.itertuples():
            (row_number, _id, parent_id, level, code, sequence, code_text, component, _property, timing, system, scale,
             method) = tpl

            if _id in id_to_code:
                raise ValueError(f'Duplicate id while reading tree "{tree_name}" for {tpl} and existing code for '
                                 f'this id is "{id_to_code[_id]}')
            id_to_code[_id] = code

        # We reiterate to do the real work
        for tpl in frame.itertuples():
            (row_number, _id, parent_id, level, code, sequence, code_text, component, _property, timing, system, scale,
             method) = tpl

            from_node_id = ll.NodeType.type_for_identifier(code).node_id_of_identifier(code)

            # save the code_text since more than a few codes are new (not in the parts file) and having this text is
            # useful in those cases

            self.add_node_attribute(node_id=from_node_id, attribute_name=ll.NodeAttributeKey.tree_code_text,
                                    attribute_value=code_text)

            # save the parent relationship

            parent_code = id_to_code.get(parent_id, None)
            if parent_code:
                to_node_id = ll.NodeType.type_for_identifier(parent_code).node_id_of_identifier(parent_code)
                self.add_edge_type(from_node_id, to_node_id, ll.EdgeType.LoincLib_HasParent)

    #######################
    # Read files as frames
    #######################

    def read_AccessoryFiles_PartFile_Part_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'AccessoryFiles' / 'PartFile' / 'Part.csv', dtype=str, na_filter=False)

    def read_AccessoryFiles_PartFile_LoincPartLink_Primary_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Primary.csv', dtype=str,
                           na_filter=False)

    def read_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'AccessoryFiles' / 'PartFile' / 'LoincPartLink_Supplementary.csv',
                           dtype=str, na_filter=False)

    def read_LoincTable_Loinc_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'LoincTable' / 'Loinc.csv', dtype=str, na_filter=False)

    def read_AccessoryFiles_ComponentHierarchyBySystem_ComponentHierarchyBySystem_csv(self) -> pd.DataFrame:
        return pd.read_csv(self.release_path / 'AccessoryFiles' / 'ComponentHierarchyBySystem' /
                           'ComponentHierarchyBySystem.csv', dtype=str, na_filter=False)

    def _read_tree(self, tree_name: str):
        return pd.read_csv(self.trees_path / f'{tree_name}.csv', dtype=str,
                           na_filter=False)


if __name__ == '__main__':
    release = Path(__file__).parent.parent.parent / 'data' / 'loinc_release' / 'extracted'

    r = LoincRelease(release, '2.7.4', '2023-06-14')

    r.parse_LoincTable_Loinc_csv()
    r.parse_AccessoryFiles_PartFile_Part_csv()

    # r.parse_AccessoryFiles_PartFile_LoincPartLink_Primary_csv()
    # r.parse_AccessoryFiles_PartFile_LoincPartLink_Supplementary_csv()

    r.parse_tree_component()
    r.parse_tree_class()
    r.parse_tree_method()
    r.parse_tree_system()
    r.parse_tree_document_ontology()
    r.parse_tree_component_by_system()

    # r.reindexEntities()

    print(f'Size of entities map: {len(r.entity_map_by_code)}')
