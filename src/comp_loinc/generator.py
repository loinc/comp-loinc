import shutil
import time
import typing as t
import urllib.parse
from pathlib import Path

import funowl
import linkml_runtime
from funowl import literals
from linkml.utils.datautils import get_dumper
from linkml_owl.dumpers import owl_dumper
from linkml_runtime.dumpers import RDFLibDumper

import loinclib as ll
from datamodel import Loinc, LoincCodeClass, PartClass, Thing, PartClassId, LoincCodeClassId, \
    LoincCodeClassNonIntersection
from loinclib import LoincEdgeType as LET, LoincAttributeType as LAT, NodeType as NT, NameSpace as NS


class Generator:
    LOINCS_LIST = 'loincs-list'
    LOINCS_PRIMARY_DEFS = 'loincs-primary-defs'
    LOINCS_SUPPLEMENTARY_DEFS = 'loincs-supplementary-defs'

    PARTS_LIST = 'parts-list'
    PARTS_TREES = 'parts-trees'
    PARTS_GROUP_CHEM_EQ = 'parts-group-chem-eq'

    GROUPS = '__groups'
    GROUP_COMP_HAS_SLASH = 'group-component-has-slash'

    def __init__(self, loinc_release: ll.LoincRelease,
                 schema_directory: Path,
                 output_directory: Path,
                 owl_output: bool,
                 rdf_output: bool):
        self.loinc_release = loinc_release
        self.schema_dir = schema_directory
        self.output_directory = output_directory

        self._owl_dumper = owl_dumper.OWLDumper()
        self.__parts: t.Dict[str, PartClass] = {}

        self.__datetime_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        self._outputs: t.Dict[str: t.Dict[str, t.List[Thing]]] = dict()
        self.owl_output: bool = owl_output
        self.rdf_output: bool = rdf_output
        self.schema_view = linkml_runtime.SchemaView(self.schema_dir / 'comp_loinc.yaml', merge_imports=True)

    def generate_loincs_list(self):

        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincCodeClass] = {}

        loincs_root = LoincCodeClass(id=_loincify('__loincs'))
        loinc_code_map['__loincs'] = loincs_root

        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            properties = self.loinc_release.get_node_properties(loinc_node_id)

            parent = self._loinc_parent(properties, loinc_code_map)

            loinc = LoincCodeClass(id=_loincify(code), subClassOf=[parent.id])
            loinc_code_map[code] = loinc

            # loinc.subClassOf.append(loincs_root.id)
            loinc.loinc_number = code

            long_common_name = properties.get(LAT.loinc_long_common_name, None)
            if long_common_name:
                loinc.long_common_name = long_common_name[0]
                loinc.label = f'_LC  {long_common_name[0]}'

            formal_name = f'{properties.get(LAT.loinc_component)[0]}'
            formal_name += f':{properties.get(LAT.loinc_property)[0]}'
            formal_name += f':{properties.get(LAT.loinc_time_aspect)[0]}'
            formal_name += f':{properties.get(LAT.loinc_system)[0]}'
            formal_name += f':{properties.get(LAT.loinc_scale_type)[0]}'
            if LAT.loinc_method_type in properties:
                formal_name += f':{properties.get(LAT.loinc_method_type)[0]}'

            loinc.formal_name = formal_name

            definitions = properties.get(LAT.loinc_definition, None)
            if definitions:
                # This is needed to work around some unusual string values that throw an error during dumping of:
                # ./LoincTable/Loinc.csv line: 47536:
                # "51947-0","Package label.Bottom panel",....
                definition = literals.Literal._to_n3(definitions[0])
                if definition:
                    loinc.description = definition

            short_name = properties.get(LAT.loinc_short_name, None)
            if short_name:
                loinc.short_name = short_name[0]

        self._outputs[Generator.LOINCS_LIST] = loinc_code_map

    def generate_loincs_primary_defs(self):

        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # component
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_COMPONENT)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple components: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_component = PartClassId(_loincify(part_code))

            # property
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_property = PartClassId(_loincify(part_code))

            # time
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_TIME)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple times: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_time = PartClassId(_loincify(part_code))

            # system
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_SYSTEM)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_system = PartClassId(_loincify(part_code))

            # scale
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_scale = PartClassId(_loincify(part_code))

            # method
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_method = PartClassId(_loincify(part_code))

        self._outputs[Generator.LOINCS_PRIMARY_DEFS] = loinc_code_map

    def generate_loincs_supplementary_defs(self):
        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # 1.1 component analyte
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_COMPONENT_analyte)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component analytes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_analyte = PartClassId(_loincify(part_code))

            # 1.2 component challenge
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_CHALLENGE_challenge)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component challenges: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_challenge = PartClassId(_loincify(part_code))

            # 1.3 component adjustment
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_ADJUSTMENT_adjustment)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component adjustments: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_adjustment = PartClassId(_loincify(part_code))

            # 1.4 component count
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_COUNT_count)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component counts: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_count = PartClassId(_loincify(part_code))

            # 2 property
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_property = PartClassId(_loincify(part_code))

            # 3.1 time core
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_TIME_time_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_time_core = PartClassId(_loincify(part_code))

            # 3.2 time modifier
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_TIME_MODIFIER_time_modifier)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time modifiers: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_time_modifier = PartClassId(_loincify(part_code))

            # 4.1 system core
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_SYSTEM_system_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_system_core = PartClassId(_loincify(part_code))

            # 4.2 system super system
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.DetailedModel_SUPER_SYSTEM_super_system)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system super systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_system_super_system = PartClassId(_loincify(part_code))

            # scale
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_scale = PartClassId(_loincify(part_code))

            # method
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.has_method = PartClassId(_loincify(part_code))

            # semantic analyte gene
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SemanticEnhancement_GENE_analyte_gene)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple semantic genes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.semantic_analyte_gene = PartClassId(_loincify(part_code))

            # syntax analyte core
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SyntaxEnhancement_COMPONENT_analyte_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_core = PartClassId(_loincify(part_code))

            # syntax analyte suffix
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SyntaxEnhancement_SUFFIX_analyte_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_suffix = PartClassId(_loincify(part_code))

            # syntax analyte divisor
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SyntaxEnhancement_DIVISOR_analyte_divisor)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_divisor = PartClassId(_loincify(part_code))

            # syntax analyte divisor suffix
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SyntaxEnhancement_SUFFIX_analyte_divisor_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor suffixes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_divisor_suffix = PartClassId(_loincify(part_code))

            # syntax analyte numerator
            parts = self.loinc_release.out_node_ids(loinc_node_id, LET.SyntaxEnhancement_NUMERATOR_analyte_numerator)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte numerators: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinc_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_numerator = PartClassId(_loincify(part_code))

        self._outputs[Generator.LOINCS_SUPPLEMENTARY_DEFS] = loinc_code_map

    def generate_group_component_has_slash(self):
        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincCodeClass] = {}

        has_slash = LoincCodeClass(id=_loincify(Generator.GROUP_COMP_HAS_SLASH))
        has_slash.subClassOf = LoincCodeClassId(_loincify(Generator.GROUPS))
        loinc_code_map[Generator.GROUP_COMP_HAS_SLASH] = has_slash

        for loinc_node_id in loinc_node_ids:

            properties = self.loinc_release.get_node_properties(loinc_node_id)

            component_names = properties.get(LAT.loinc_component, None)
            if component_names:
                component_name = component_names[0]
                part_1 = component_name.split('^')[0]
                if '/' not in part_1:
                    continue
            else:
                continue

            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = LoincCodeClass(id=_loincify(code))
            loinc.subClassOf = has_slash.id
            loinc_code_map[code] = loinc

        self._outputs[Generator.GROUP_COMP_HAS_SLASH] = loinc_code_map

    def generate_parts_list(self):
        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_part)
        code_part_map: t.Dict[str, PartClass] = {}

        for part_node_id in part_node_ids:
            code = NT.loinc_part.identifier_of_nodeid(part_node_id)
            properties: dict = self.loinc_release.get_node_properties(part_node_id)
            part_name = properties.get(LAT.part_name, [None])[0]
            part_display_name = properties.get(LAT.part_display_name, [None])[0]
            part_type = properties.get(LAT.part_type, [None])[0]

            part = PartClass(id=_loincify(code), part_number=code)

            if part_name:
                part.label = part_name
                part.part_name = part_name
            if part_display_name:
                part.part_display_name = part_display_name

            if part_type:
                part.part_type = part_type

            code_part_map[code] = part

        self._outputs[Generator.PARTS_LIST] = code_part_map

    def generate_parts_trees(self):

        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_part)
        code_part_map: t.Dict[str, PartClass] = {}

        parts_hierarchy_root = PartClass(id=_loincify('__parts_trees'))
        parts_no_hierarchy_root = PartClass(id=_loincify('__parts_no_hierarchy'))

        code_part_map['__parts_trees'] = parts_hierarchy_root
        code_part_map['__parts_no_hierarchy'] = parts_no_hierarchy_root

        for part_node_id in part_node_ids:
            loinc_part_identifier = NT.loinc_part.identifier_of_nodeid(part_node_id)
            part = PartClass(id=_loincify(loinc_part_identifier))
            code_part_map[loinc_part_identifier] = part

            properties = self.loinc_release.get_node_properties(part_node_id)

            # Do annotations.
            # Is this a new part code?
            if LAT.part_name not in properties:
                # this code is not in the parts file
                part.part_number = loinc_part_identifier
                code_text = properties.get(LAT.tree_code_text, None)
                if code_text:
                    part.label = f'_tree_label_ {code_text[0]}'

            # do subclass axioms
            parent_ids = self.loinc_release.out_node_ids(part_node_id, LET.LoincTree_has_parent_has_parent)
            if parent_ids:
                part.subClassOf = [_loincify(NT.loinc_part.identifier_of_nodeid(parent_id)) for
                                   parent_id in parent_ids.values()]
            else:
                part_parent = None
                child_node_ids = self.loinc_release.in_node_ids(part_node_id, LET.LoincTree_has_parent_has_parent)
                for _, child_of_child_node_id in child_node_ids.items():
                    child_node_type = NT.type_for_node_id(child_of_child_node_id)
                    if child_node_type and child_node_type == NT.loinc_part:
                        part_parent = parts_hierarchy_root
                        break

                if not part_parent:
                    part_parent = parts_no_hierarchy_root
                part.subClassOf.append(part_parent)

        self._outputs[Generator.PARTS_TREES] = code_part_map

    def generate_parts_group_chem_equivalences(self):

        code_map: dict[str, LoincCodeClass] = {}

        group = LoincCodeClass(id=_loincify('__parts-group-comp-eq'))
        group.subClassOf = LoincCodeClassId(Generator.GROUPS)
        code_map[group.id] = group

        chem_node_id = NT.loinc_part.nodeid_of_identifier('LP7786-9')
        chem = self._parts_group_comp_equivalences_recurse(chem_node_id, code_map)
        chem.subClassOf = group.id

        self._outputs[Generator.PARTS_GROUP_CHEM_EQ] = code_map


    def _parts_group_comp_equivalences_recurse(self, part_node_id, code_map):
        code = NT.loinc_part.identifier_of_nodeid(part_node_id)
        properties = self.loinc_release.get_node_properties(part_node_id)

        part_based_def = LoincCodeClassNonIntersection(id=_loincify(f'{code}_comp_eq'))

        label = None
        part_names = properties.get(LAT.part_name, None)
        if part_names:
            label = f'{part_names[0]} (COMP EQ)'
        if not label:
            code_texts = properties.get(LAT.tree_code_text)
            if code_texts:
                label = f'{code_texts[0]} (COMP EQ)'
        if not label:
            label = f'{code} (COMP EQ)'

        part_based_def.label = label
        part_based_def.has_component = PartClass(id=_loincify(code))
        code_map[code] = part_based_def

        children_parts = self.loinc_release.in_node_ids(part_node_id, LET.LoincTree_has_parent_has_parent).values()
        for child_part_id in children_parts:
            if NT.type_for_node_id(child_part_id) == NT.loinc_part:
                child_def = self._parts_group_comp_equivalences_recurse(child_part_id, code_map)
                child_def.subClassOf.append(part_based_def.id)

        return part_based_def

    def generate_chebi_mappings(self):
        self._generate_mapping(ll.NameSpace.chebi)

    def _generate_mapping(self, namespace: ll.NameSpace):
        target_node_type = ll.NodeType.nodetype_for_namespace(namespace)
        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_part)

        part_map: dict[str, Thing] = {}

        for part_node_id in part_node_ids:
            part_identifier = ll.NodeType.loinc_part.identifier_of_nodeid(part_node_id)
            # equivalence axioms
            equivalent_target_node_ids = self.loinc_release.out_node_ids(part_node_id,
                                                                         LET.Equivalence_equivalent_equivalent)
            for equivalent_target_node_id in [id for key, id in equivalent_target_node_ids.items() if
                                              target_node_type.is_type_of_nodeid(id)]:
                loinc_part = part_map.setdefault(part_identifier,
                                                 PartClass(NS.loinc.owl_url(part_identifier)))
                target: Thing = Thing(
                    namespace.owl_url(target_node_type.identifier_of_nodeid(equivalent_target_node_id)))
                properties = self.loinc_release.get_node_properties(equivalent_target_node_id)
                displays = properties.get(LAT.display, None)
                if displays:
                    target.label = displays[0]
                loinc_part.equivalentClasses.append(target)


        self._outputs[f'mapping-{namespace.node_id_prefix}-equivalence'] = part_map

    def save_outputs(self):
        for filename, output in self._outputs.items():
            if self.owl_output:
                self._write_owl_outputs(output_name=filename)
            if self.rdf_output:
                self._write_rdf_outputs(output_name=filename)

        self._outputs.clear()

    def _write_owl_outputs(self, /, *,
                           output_name: str,
                           timestamped=True):
        output_file = self.output_directory / f'{output_name}.owl'
        output_file_datetime = self.output_directory / 'datetime' / f'{output_name}_{self.__datetime_string}.owl'

        output_file_datetime.parent.mkdir(parents=True, exist_ok=True)
        print(f'Writing: {output_file_datetime}', flush=True)
        document: funowl.ontology_document.OntologyDocument = \
            self._owl_dumper.to_ontology_document(element=list(self._outputs[output_name].values()),
                                                  schema=self.schema_view.schema)
        document.ontology.iri = funowl.identifiers.IRI(f'https://loinc.org/{output_name}')

        with open(output_file_datetime, 'w') as f:
            f.write(str(document))
        if timestamped:
            shutil.copyfile(output_file_datetime, output_file)
        else:
            shutil.move(output_file_datetime, output_file)

    def _write_rdf_outputs(self, /, *,
                           output_name: str,
                           timestamped=True):
        output_file = self.output_directory / f'{output_name}.ttl'
        output_file_datetime = self.output_directory / 'datetime' / f'{output_name}_{self.__datetime_string}.ttl'

        output_file_datetime.parent.mkdir(parents=True, exist_ok=True)
        print(f'Writing: {output_file_datetime}', flush=True)

        entities = list(self._outputs[output_name].values())
        if len(entities) > 0:
            loinc: Loinc = Loinc()
            entity = entities[0]

            if isinstance(entity, LoincCodeClass):
                loinc.codes = entities
            elif isinstance(entity, PartClass):
                loinc.parts = entities

            dumper: RDFLibDumper = get_dumper('ttl')
            dumper.dump(element=loinc,
                        to_file=str(output_file_datetime),
                        schemaview=self.schema_view,
                        prefix_map={'@base': 'http://example'})

    def _loinc_parent(self, properties, code_map: dict[str, LoincCodeClass]) -> LoincCodeClass:

        class_types = properties.get(LAT.loinc_class_type, None)
        class_type = None
        if class_types:
            class_type_code = f'classtype_{class_types[0]}'
            class_type = code_map.setdefault(class_type_code, LoincCodeClass(id=_loincify(class_type_code),
                                                                             label=f'class type {class_types[0]}',
                                                                             subClassOf=[
                                                                                 code_map['__loincs'].id
                                                                             ]
                                                                             ))

        classes = properties.get(LAT.loinc_class, None)
        class_part = None
        if classes:
            class_parts = classes[0].split('.')
            url_suffix = None
            for part in class_parts:
                if not class_part:
                    url_suffix = f'class_{part}'

                    class_part = code_map.setdefault(url_suffix, LoincCodeClass(
                        id=_loincify(urllib.parse.quote(url_suffix))))
                    class_part.subClassOf = [class_type.id]
                    continue
                else:
                    url_suffix = f'{url_suffix}.{part}'
                    class_part = code_map.setdefault(url_suffix,
                                                     LoincCodeClass(
                                                         id=_loincify(urllib.parse.quote(url_suffix)),
                                                         subClassOf=[class_part.id]))

        return class_part


def _loincify(identifier) -> str:
    """
    adds the loinc: prefix to loinc part and code numbers
    :param identifier:
    :return: string
    """
    if identifier == 'owl:Thing':
        return identifier

    return f"loinc:{identifier}"
