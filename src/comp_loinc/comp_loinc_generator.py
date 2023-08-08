import shutil
import time
import typing as t
from pathlib import Path

import funowl
import linkml_runtime
from funowl import literals
from linkml_owl.dumpers import owl_dumper

import loinclib as ll
from comp_loinc import datamodel


class CompLoincGenerator:
    LOINCS_LIST = 'loincs-list'
    LOINCS_PARTS_EQUIVALENCE = 'loincs-parts-eq'

    LOINCS_GROUP_COMPONENT_SUBPART_ONE_HAS_SLASH = 'loincs-group-component_subpart_one_has_slash'

    PARTS_LIST = 'parts-list'
    PARTS_TREES = 'parts-trees'

    PARTS_GROUP_CHEM_EQ = 'parts-group-chem-eq'

    def __init__(self, loinc_release: ll.LoincRelease,
                 schema_directory: Path,
                 output_directory: Path):
        self.release = loinc_release
        self.schema_dir = schema_directory
        self.output_directory = output_directory

        self._owl_dumper = owl_dumper.OWLDumper()
        self.__parts: t.Dict[str, datamodel.PartClass] = {}

        self.__datetime_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        self._outputs: t.Dict[str: t.Dict[str, t.List[datamodel.Thing]]] = dict()
        self._outputs_schema: t.Dict[str, linkml_runtime.SchemaView] = dict()

    def generate_loincs_list(self):

        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        loincs_root = datamodel.LoincCodeClass(id=_loincify('__loincs'))
        loinc_code_map['__loincs'] = loincs_root

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc
            properties = self.release.node_properties(loinc_node_id)

            loinc.subClassOf.append(loincs_root.id)
            loinc.loinc_number = code

            long_common_name = properties.get(ll.NodeAttributeKey.loinc_long_common_name, None)
            if long_common_name:
                loinc.long_common_name = long_common_name[0]
                loinc.label = f'_L  {long_common_name[0]}'

            formal_name = f'{properties.get(ll.NodeAttributeKey.loinc_component)[0]}'
            formal_name += f':{properties.get(ll.NodeAttributeKey.loinc_property)[0]}'
            formal_name += f':{properties.get(ll.NodeAttributeKey.loinc_time_aspect)[0]}'
            formal_name += f':{properties.get(ll.NodeAttributeKey.loinc_system)[0]}'
            formal_name += f':{properties.get(ll.NodeAttributeKey.loinc_scale_type)[0]}'
            if ll.NodeAttributeKey.loinc_method_type in properties:
                formal_name += f':{properties.get(ll.NodeAttributeKey.loinc_method_type)[0]}'

            loinc.formal_name = formal_name

            definitions = properties.get(ll.NodeAttributeKey.loinc_definition, None)
            if definitions:
                # This is needed to work around some unusual string values that throw an error during dumping of:
                # ./LoincTable/Loinc.csv line: 47536:
                # "51947-0","Package label.Bottom panel",....
                definition = literals.Literal._to_n3(definitions[0])
                if definition:
                    loinc.description = definition

            short_name = properties.get(ll.NodeAttributeKey.loinc_short_name, None)
            if short_name:
                loinc.short_name = short_name[0]

        self._outputs[CompLoincGenerator.LOINCS_LIST] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_LIST] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def save_outputs(self):
        for filename, output in self._outputs.items():
            self._write_outputs(output_name=filename)

    def generate_loincs_defs(self):

        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # component
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_COMPONENT)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple components: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component = datamodel.PartClassId(_loincify(part_code))

            # property
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_property = datamodel.PartClassId(_loincify(part_code))

            # time
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_TIME)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple times: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_time = datamodel.PartClassId(_loincify(part_code))

            # system
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_SYSTEM)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_system = datamodel.PartClassId(_loincify(part_code))

            # scale
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_scale = datamodel.PartClassId(_loincify(part_code))

            # method
            parts = self.release.out_node_ids(loinc_node_id, ll.LoincPrimaryEdgeType.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_method = datamodel.PartClassId(_loincify(part_code))

        self._outputs[CompLoincGenerator.LOINCS_PARTS_EQUIVALENCE] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_PARTS_EQUIVALENCE] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def generate_parts_list(self):
        part_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        # parts_root = datamodel.PartClass(id=_loincify('__parts'))
        # code_part_map['__parts'] = parts_root

        for part_node_id in part_node_ids:
            code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
            properties: dict = self.release.node_properties(part_node_id)
            part_name = properties.get(ll.NodeAttributeKey.part_name, [None])[0]
            part_display_name = properties.get(ll.NodeAttributeKey.part_display_name, [None])[0]
            part_type = properties.get(ll.NodeAttributeKey.part_type, [None])[0]

            part = datamodel.PartClass(id=_loincify(code), part_number=code)
            # part.subClassOf.append(parts_root)

            if part_name:
                part.label = part_name
                part.part_name = part_name
            if part_display_name:
                part.part_display_name = part_display_name

            if part_type:
                part.part_type = part_type

            code_part_map[code] = part

        self._outputs[CompLoincGenerator.PARTS_LIST] = code_part_map
        self._outputs_schema[CompLoincGenerator.PARTS_LIST] = linkml_runtime.SchemaView(
            self.schema_dir / 'part_schema.yaml')

    def generate_parts_trees(self):

        part_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        parts_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_trees'))
        parts_no_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_no_hierarchy'))

        code_part_map['__parts_trees'] = parts_hierarchy_root
        code_part_map['__parts_no_hierarchy'] = parts_no_hierarchy_root

        for part_node_id in part_node_ids:
            part_code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)
            part = datamodel.PartClass(id=_loincify(part_code))
            code_part_map[part_code] = part

            properties = self.release.node_properties(part_node_id)

            # Do annotations.
            # Is this a new part code?
            if ll.NodeAttributeKey.part_name not in properties:
                # this code is not in the parts file
                part.part_number = part_code
                code_text = properties.get(ll.NodeAttributeKey.tree_code_text, None)
                if code_text:
                    part.label = f'_tree_label_ {code_text[0]}'

            # do subclass axioms
            parent_ids = self.release.out_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent)
            if parent_ids:
                part.subClassOf = [_loincify(ll.NodeType.loinc_part.identifier_of_node_id(parent_id)) for
                                   parent_id in parent_ids.values()]
            else:
                part_parent = None
                child_node_ids = self.release.in_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent)
                for _, child_of_child_node_id in child_node_ids.items():
                    child_node_type = ll.NodeType.type_for_node_id(child_of_child_node_id)
                    if child_node_type and child_node_type == ll.NodeType.loinc_part:
                        part_parent = parts_hierarchy_root
                        break

                if not part_parent:
                    part_parent = parts_no_hierarchy_root
                part.subClassOf.append(part_parent)

        self._outputs[CompLoincGenerator.PARTS_TREES] = code_part_map
        self._outputs_schema[CompLoincGenerator.PARTS_TREES] = linkml_runtime.SchemaView(
            self.schema_dir / 'part_schema.yaml')

    def parts_group_chem_equivalences(self):

        code_map: dict[str, datamodel.LoincCodeClass] = {}

        group = datamodel.LoincCodeClass(id=_loincify('__parts-group-comp-eq'))
        code_map[group.id] = group

        chem_node_id = ll.NodeType.loinc_part.node_id_of_identifier('LP7786-9')
        chem = self._parts_group_comp_equivalences_recurse(chem_node_id, code_map)
        # chem.subClassOf.append(group.id)

        self._outputs[CompLoincGenerator.PARTS_GROUP_CHEM_EQ] = code_map
        code_view = linkml_runtime.SchemaView(self.schema_dir / 'code_schema.yaml')
        part_view = linkml_runtime.SchemaView(self.schema_dir / 'part_schema.yaml')
        code_view.merge_schema(part_view.schema)
        self._outputs_schema[CompLoincGenerator.PARTS_GROUP_CHEM_EQ] = code_view

    def _parts_group_comp_equivalences_recurse(self, part_node_id, code_map):
        code = ll.NodeType.loinc_part.identifier_of_node_id(part_node_id)

        properties = self.release.node_properties(part_node_id)
        part_based_def = datamodel.LoincCodeClass(id=_loincify(f'{code}_comp_eq'))

        label = None
        part_names = properties.get(ll.NodeAttributeKey.part_name, None)
        if part_names:
            label = f'{part_names[0]} (COMP EQ)'
        if not label:
            code_texts = properties.get(ll.NodeAttributeKey.tree_code_text)
            if code_texts:
                label = f'{code_texts[0]} (COMP EQ)'
        if not label:
            label = f'{code} (COMP EQ)'

        part_based_def.label = label
        part_based_def.has_component = datamodel.PartClass(id=_loincify(code))
        code_map[code] = part_based_def

        children_parts = self.release.in_node_ids(part_node_id, ll.EdgeType.LoincLib_HasParent).values()
        for child_part_id in children_parts:
            if ll.NodeType.type_for_node_id(child_part_id) == ll.NodeType.loinc_part:
                child_def = self._parts_group_comp_equivalences_recurse(child_part_id, code_map)
                # child_def.subClassOf.append(part_based_def.id)

        return part_based_def

    def generate_loincs_group_component_subpart_one_has_slash(self):
        loinc_node_ids = self.release.node_ids_for_type(ll.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        loincs_group = datamodel.LoincCodeClass(id=_loincify('__loincs_group_component_subpart_one_has_slash'))
        loinc_code_map[loincs_group.id] = loincs_group

        for loinc_node_id in loinc_node_ids:
            code = ll.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            properties = self.release.node_properties(loinc_node_id)
            components = properties.get(ll.NodeAttributeKey.loinc_component, None)
            if components:
                component: str = components[0]
                subpart_one = component.split('^')[0]
                if '/' in subpart_one:
                    loinc.subClassOf.append(loincs_group
                                            .id)
                    loinc_code_map[code] = loinc

        self._outputs[CompLoincGenerator.LOINCS_GROUP_COMPONENT_SUBPART_ONE_HAS_SLASH] = loinc_code_map
        self._outputs_schema[
            CompLoincGenerator.LOINCS_GROUP_COMPONENT_SUBPART_ONE_HAS_SLASH] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def _write_outputs(self, /, *,
                       output_name: str,
                       timestamped=True):
        output_file = self.output_directory / f'{output_name}.owl'
        output_file_datetime = self.output_directory / 'datetime' / f'{output_name}_{self.__datetime_string}.owl'

        output_file_datetime.parent.mkdir(parents=True, exist_ok=True)
        print(f'Writing: {output_file_datetime}', flush=True)
        document: funowl.ontology_document.OntologyDocument = \
            self._owl_dumper.to_ontology_document(element=list(self._outputs[output_name].values()),
                                                  schema=self._outputs_schema[output_name].schema)
        document.ontology.iri = funowl.identifiers.IRI(f'https://loinc.org/{output_name}')

        with open(output_file_datetime, 'w') as f:
            f.write(str(document))
        if timestamped:
            shutil.copyfile(output_file_datetime, output_file)
        else:
            shutil.move(output_file_datetime, output_file)


def _loincify(id) -> str:
    """
    adds the loinc: prefix to loinc part and code numbers
    :param id:
    :return: string
    """
    if id == 'owl:Thing':
        return id

    return f"loinc:{id}"
