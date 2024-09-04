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
from comp_loinc.datamodel import Loinc, LoincTerm, LoincPart, LoincEntity, PartClassId, LoincTermId, \
    LoincTermIntersection, LoincTermNonIntersection
from comp_loinc.datamodel import LoincTermNonIntersectionId
from loinclib import NodeType as NT, NameSpaceEnum as NS, PropertyType as PT, EdgeType as ET


class Generator:
    LOINCS_LIST = 'loincs-list'
    LOINCS_PRIMARY_DEFS = 'loincs-primary-defs'
    LOINCS_SUPPLEMENTARY_DEFS = 'loincs-supplementary-defs'

    PARTS_LIST = 'parts-list'
    PARTS_TREES = 'parts-trees'
    PARTS_GROUP_CHEM_EQ = 'parts-group-chem-eq'

    GROUPS = '__groups'
    GROUP_COMP_HAS_SLASH = 'group-component-has-slash'

    def __init__(self, loinc_release: ll.Graph,
                 schema_directory: Path,
                 output_directory: Path,
                 owl_output: bool,
                 rdf_output: bool):
        self.loinc_release = loinc_release
        self.schema_dir = schema_directory
        self.output_directory = output_directory
        self.owl_output: bool = owl_output
        self.rdf_output: bool = rdf_output

        self.loincs: dict[str, t.Union[LoincTerm, None]] = {}
        self.parts: dict[str, t.Union[LoincPart]] = {}

        self._owl_dumper = owl_dumper.OWLDumper()
        self.__parts: t.Dict[str, LoincPart] = {}

        self.__datetime_string = time.strftime('%Y-%m-%d_%H-%M-%S')

        self._outputs: t.Dict[str, t.Dict[str, LoincEntity]] = dict()
        self.schema_view = linkml_runtime.SchemaView(self.schema_dir / 'comp_loinc.yaml', merge_imports=True)

    def add_part_info(self, part_codes: list[str] = None):
        if part_codes:
            self.add_part_codes(part_codes)
        else:
            part_codes = list(self.parts.keys())

        for part_code in part_codes:
            node_id = NT.loinclib_part.nodeid_of_identifier(part_code)
            part = self.get_part(part_code=part_code, part_class=LoincPart)

            part_name = self.loinc_release.get_first_node_property(PT.loinc_part_name, node_id)
            part.label = part_name
            part.part_name = part_name
            part.part_display_name = self.loinc_release.get_first_node_property(PT.loinc_part_display_name, node_id)
            part.part_type = self.loinc_release.get_first_node_property(PT.loinc_part_type, node_id)

    def add_loincs_codes(self, loinc_codes: list[str]):
        """Set the LOINC codes that will be processed.

        The provided codes will be added to any existing codes."""
        for loinc_code in loinc_codes:
            if loinc_code not in self.loincs:
                self.loincs[loinc_code] = None

    def add_part_codes(self, part_codes: list[str]):
        """Set the LOINC Part codes that will be processed.

        The provided codes will be added to any existing codes."""
        for part_code in part_codes:
            if part_code not in self.parts:
                self.parts[part_code] = None

    def get_part(self, part_code: str, part_class: t.Type[LoincPart]) -> LoincPart:
        part = self.parts.get(part_code, ...)
        if part is None:
            part = part_class(_loincify(part_code))
            part.part_number = part_code
            self.parts[part_code] = part
        elif part is ...:
            part = None
        return part

    def get_loinc(self, loinc_code: str, loinc_class: t.Type[LoincTerm]) -> LoincPart:
        loinc = self.loincs.get(loinc_code, ...)
        if loinc is None:
            loinc = loinc_class(_loincify(loinc_code))
            loinc.loinc_number = loinc_code
            self.loincs[loinc_code] = loinc
        elif loinc is ...:
            loinc = None
        return loinc

    def save_owl(self, group_name: str):
        pass

    ############################

    def generate_parts_list(self):
        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinclib_part)
        code_part_map: t.Dict[str, LoincPart] = {}

        for part_node_id in part_node_ids:
            code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
            part = self.parts.setdefault(code, LoincPart(id=_loincify(code), part_number=code))

            part_name = self.loinc_release.get_first_node_property(PT.loinc_part_name, part_node_id)
            part.label = part_name
            part.part_name = part_name

            part.part_display_name = self.loinc_release.get_first_node_property(PT.loinc_part_display_name,
                                                                                part_node_id)
            part.part_type = self.loinc_release.get_first_node_property(PT.loinc_part_type, part_node_id)

            code_part_map[code] = part

        self._outputs[Generator.PARTS_LIST] = code_part_map

    #############################

    def generate_loincs_list(self):

        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        # loinc_code_map: dict[str, LoincCodeClass] = {}

        loincs_root = LoincTermIntersection(id=_loincify('__loincs'))
        self.loincs['__loincs'] = loincs_root

        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            properties = self.loinc_release.get_node_properties(loinc_node_id)

            parent = self._loinc_parent(properties, self.loincs)
            parent_id: LoincTermId = LoincTermId(parent.id)

            # TODO: SE: there must be a better way (in Python) to check and add to list if needed, by attribute value(e)
            # How do LinkML objects implement __eq__?  Specifically the *Id classes?
            loinc = self.loincs.setdefault(code, LoincTermIntersection(id=_loincify(code)))
            parents = loinc.subClassOf
            if parents:
                has_parent = False
                p: LoincTermId
                for p in parents:
                    if p == parent_id:
                        has_parent = True

                if not has_parent:
                    loinc.subClassOf.append(parent_id)

            else:
                loinc.subClassOf.append(parent_id)

            # loinc = LoincCodeClassIntersection(id=_loincify(code), subClassOf=[LoincCodeClassId(parent.id)])
            # self.loincs[code] = loinc
            # loinc_code_map[code] = loinc

            # loinc.subClassOf.append(loincs_root.id)
            loinc.loinc_number = code

            long_common_name = properties.get(PT.loinc_long_common_name, None)
            if long_common_name:
                loinc.long_common_name = long_common_name[0]
                loinc.label = f'_LC  {long_common_name[0]}'

            formal_name = f'{properties.get(PT.loinc_component)[0]}'
            formal_name += f':{properties.get(PT.loinc_property)[0]}'
            formal_name += f':{properties.get(PT.loinc_time_aspect)[0]}'
            formal_name += f':{properties.get(PT.loinc_system)[0]}'
            formal_name += f':{properties.get(PT.loinc_scale_type)[0]}'
            if PT.loinc_method_type in properties:
                formal_name += f':{properties.get(PT.loinc_method_type)[0]}'

            loinc.formal_name = formal_name

            definitions = properties.get(PT.loinc_definition, None)
            if definitions:
                # This is needed to work around some unusual string values that throw an error during dumping of:
                # ./LoincTable/Loinc.csv line: 47536:
                # "51947-0","Package label.Bottom panel",....
                definition = literals.Literal._to_n3(definitions[0])
                if definition:
                    loinc.description = definition

            short_name = properties.get(PT.loinc_short_name, None)
            if short_name:
                loinc.short_name = short_name[0]

            loinc_class = properties.get(PT.loinc_class, None)
            if loinc_class:
                loinc.loinc_class = loinc_class[0]

            loinc_class_type = properties.get(PT.loinc_class_type, None)
            if loinc_class_type:
                loinc.loinc_class_type = loinc_class_type[0]

        self._outputs[Generator.LOINCS_LIST] = self.loincs

    def generate_loincs_primary_defs(self):

        loinc_code_map: dict[str, LoincTerm] = {}

        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = self.loincs.setdefault(code, LoincTermIntersection(id=_loincify(code)))

            loinc.loinc_number = code
            loinc_properties = self.loinc_release.get_node_properties(loinc_node_id)
            common_name = loinc_properties.get(PT.loinc_long_common_name, None)
            if common_name:
                loinc.long_common_name = common_name[0];
            loinc_code_map[code] = loinc

            # component
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_COMPONENT)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple components: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_component = PartClassId(_loincify(part_code))

            # property
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_property = PartClassId(_loincify(part_code))

            # time
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_TIME)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple times: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_time = PartClassId(_loincify(part_code))

            # system
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_SYSTEM)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_system = PartClassId(_loincify(part_code))

            # scale
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_scale = PartClassId(_loincify(part_code))

            # method
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_method = PartClassId(_loincify(part_code))

        self._outputs[Generator.LOINCS_PRIMARY_DEFS] = loinc_code_map

    def generate_loincs_supplementary_defs(self):
        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincTerm] = {}

        for loinc_node_id in loinc_node_ids:
            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = LoincTermIntersection(id=_loincify(code))
            loinc_code_map[code] = loinc

            # 1.1 component analyte
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_COMPONENT_analyte)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component analytes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_analyte = PartClassId(_loincify(part_code))

            # 1.2 component challenge
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_CHALLENGE_challenge)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component challenges: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_challenge = PartClassId(_loincify(part_code))

            # 1.3 component adjustment
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_ADJUSTMENT_adjustment)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component adjustments: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_adjustment = PartClassId(_loincify(part_code))

            # 1.4 component count
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_COUNT_count)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple component counts: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_component_count = PartClassId(_loincify(part_code))

            # 2 property
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_property = PartClassId(_loincify(part_code))

            # 3.1 time core
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_TIME_time_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_time_core = PartClassId(_loincify(part_code))

            # 3.2 time modifier
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_TIME_MODIFIER_time_modifier)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple time modifiers: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_time_modifier = PartClassId(_loincify(part_code))

            # 4.1 system core
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_SYSTEM_system_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system cores: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_system_core = PartClassId(_loincify(part_code))

            # 4.2 system super system
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_DetailedModel_SUPER_SYSTEM_super_system)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple system super systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_system_super_system = PartClassId(_loincify(part_code))

            # scale
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_scale = PartClassId(_loincify(part_code))

            # method
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.has_method = PartClassId(_loincify(part_code))

            # semantic analyte gene
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_SemanticEnhancement_GENE_analyte_gene)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple semantic genes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.semantic_analyte_gene = PartClassId(_loincify(part_code))

            # syntax analyte core
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_SyntaxEnhancement_COMPONENT_analyte_core)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_core = PartClassId(_loincify(part_code))

            # syntax analyte suffix
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_SyntaxEnhancement_SUFFIX_analyte_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte core: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_suffix = PartClassId(_loincify(part_code))

            # syntax analyte divisor
            parts = self.loinc_release.out_node_ids(loinc_node_id, ET.loinc_SyntaxEnhancement_DIVISOR_analyte_divisor)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_divisor = PartClassId(_loincify(part_code))

            # syntax analyte divisor suffix
            parts = self.loinc_release.out_node_ids(loinc_node_id,
                                                    ET.loinc_SyntaxEnhancement_SUFFIX_analyte_divisor_suffix)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte divisor suffixes: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_divisor_suffix = PartClassId(_loincify(part_code))

            # syntax analyte numerator
            parts = self.loinc_release.out_node_ids(loinc_node_id,
                                                    ET.loinc_SyntaxEnhancement_NUMERATOR_analyte_numerator)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple syntax analyte numerators: {parts}')
            for key, part_node_id in parts.items():
                part_code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
                loinc.syntax_analyte_numerator = PartClassId(_loincify(part_code))

        self._outputs[Generator.LOINCS_SUPPLEMENTARY_DEFS] = loinc_code_map

    def generate_group_component_has_slash(self):
        loinc_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinc_code)
        loinc_code_map: dict[str, LoincTerm] = {}

        has_slash = LoincTermIntersection(id=_loincify(Generator.GROUP_COMP_HAS_SLASH))
        has_slash.subClassOf = [LoincTermId(_loincify(Generator.GROUPS))]
        loinc_code_map[Generator.GROUP_COMP_HAS_SLASH] = has_slash

        for loinc_node_id in loinc_node_ids:

            properties = self.loinc_release.get_node_properties(loinc_node_id)

            component_names = properties.get(PT.loinc_component, None)
            if component_names:
                component_name = component_names[0]
                part_1 = component_name.split('^')[0]
                if '/' not in part_1:
                    continue
            else:
                continue

            code = NT.loinc_code.identifier_of_nodeid(loinc_node_id)
            loinc = LoincTermIntersection(id=_loincify(code))
            loinc.subClassOf = [LoincTermId(has_slash.id)]
            loinc_code_map[code] = loinc

        self._outputs[Generator.GROUP_COMP_HAS_SLASH] = loinc_code_map

    def generate_parts_trees(self):

        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinclib_part)
        code_part_map: t.Dict[str, LoincPart] = {}

        parts_hierarchy_root = LoincPart(id=_loincify('__parts_trees'))
        parts_no_hierarchy_root = LoincPart(id=_loincify('__parts_no_hierarchy'))

        code_part_map['__parts_trees'] = parts_hierarchy_root
        code_part_map['__parts_no_hierarchy'] = parts_no_hierarchy_root

        for part_node_id in part_node_ids:
            loinc_part_identifier = NT.loinclib_part.identifier_of_nodeid(part_node_id)
            part = LoincPart(id=_loincify(loinc_part_identifier))
            code_part_map[loinc_part_identifier] = part

            properties = self.loinc_release.get_node_properties(part_node_id)

            # Do annotations.
            # Is this a new part code?
            if PT.loinc_part_name not in properties:
                # this code is not in the parts file
                part.part_number = loinc_part_identifier
                code_text = properties.get(PT.loinc_tree_code_text, None)
                if code_text:
                    part.label = f'_tree_label_ {code_text[0]}'

            # do subclass axioms
            parent_ids = self.loinc_release.out_node_ids(part_node_id, ET.loinc_LoincTree_has_parent_has_parent)
            if parent_ids:
                part.subClassOf = [PartClassId(_loincify(NT.loinclib_part.identifier_of_nodeid(parent_id))) for
                                   parent_id in parent_ids.values()]
            else:
                part_parent = None
                child_node_ids = self.loinc_release.in_node_ids(part_node_id, ET.loinc_LoincTree_has_parent_has_parent)
                for _, child_of_child_node_id in child_node_ids.items():
                    child_node_type = NT.type_for_node_id(child_of_child_node_id)
                    if child_node_type and child_node_type == NT.loinclib_part:
                        part_parent = parts_hierarchy_root
                        break

                if not part_parent:
                    part_parent = parts_no_hierarchy_root
                part.subClassOf.append(PartClassId(part_parent.id))

        self._outputs[Generator.PARTS_TREES] = code_part_map

    def generate_parts_group_chem_equivalences(self):

        code_map: dict[str, LoincTerm] = {}

        group = LoincTermIntersection(id=_loincify('__parts-group-comp-eq'))
        group.subClassOf = [LoincTermId(Generator.GROUPS)]
        code_map[group.id] = group

        chem_node_id = NT.loinclib_part.nodeid_of_identifier('LP7786-9')
        chem = self._parts_group_comp_equivalences_recurse(chem_node_id, code_map)
        chem.subClassOf = [LoincTermId(group.id)]

        self._outputs[Generator.PARTS_GROUP_CHEM_EQ] = code_map

    def _parts_group_comp_equivalences_recurse(self, part_node_id, code_map):
        code = NT.loinclib_part.identifier_of_nodeid(part_node_id)
        properties = self.loinc_release.get_node_properties(part_node_id)

        part_based_def = LoincTermNonIntersection(id=_loincify(f'{code}_comp_eq'))

        label = None
        part_names = properties.get(PT.loinc_part_name, None)
        if part_names:
            label = f'{part_names[0]} (COMP EQ)'
        if not label:
            code_texts = properties.get(PT.loinc_tree_code_text)
            if code_texts:
                label = f'{code_texts[0]} (COMP EQ)'
        if not label:
            label = f'{code} (COMP EQ)'

        part_based_def.entity_labels = label
        part_based_def.has_component = LoincPart(id=_loincify(code))
        code_map[code] = part_based_def

        children_parts = self.loinc_release.in_node_ids(part_node_id, ET.loinc_LoincTree_has_parent_has_parent).values()
        for child_part_id in children_parts:
            if NT.type_for_node_id(child_part_id) == NT.loinclib_part:
                child_def = self._parts_group_comp_equivalences_recurse(child_part_id, code_map)
                child_def.subClassOf.append(LoincTermNonIntersectionId(part_based_def.id))

        return part_based_def

    def generate_chebi_mappings(self):
        self._generate_mapping(ll.NameSpaceEnum.chebi)

    def _generate_mapping(self, namespace: ll.NameSpaceEnum):
        target_node_type = ll.NodeType.nodetype_for_namespace(namespace)
        part_node_ids = self.loinc_release.get_all_node_ids_for_node_type(NT.loinclib_part)

        part_map: dict[str, LoincEntity] = {}

        for part_node_id in part_node_ids:
            part_identifier = ll.NodeType.loinclib_part.identifier_of_nodeid(part_node_id)
            # equivalence axioms
            equivalent_target_node_ids = self.loinc_release.out_node_ids(part_node_id,
                                                                         ET.loinc_Equivalence_equivalent_equivalent)
            for equivalent_target_node_id in [id for key, id in equivalent_target_node_ids.items() if
                                              target_node_type.is_type_of_nodeid(id)]:
                loinc_part = part_map.setdefault(part_identifier,
                                                 LoincPart(NS.loinc.owl_url(part_identifier)))
                target: LoincEntity = LoincEntity(
                    namespace.owl_url(target_node_type.identifier_of_nodeid(equivalent_target_node_id)))
                properties = self.loinc_release.get_node_properties(equivalent_target_node_id)
                displays = properties.get(PT.loinc_display, None)
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

            if isinstance(entity, LoincTerm):
                loinc.codes = entities
            elif isinstance(entity, LoincPart):
                loinc.parts = entities

            dumper: RDFLibDumper = get_dumper('ttl')
            dumper.dump(element=loinc,
                        to_file=str(output_file_datetime),
                        schemaview=self.schema_view,
                        prefix_map={'@base': 'http://example'})
            if timestamped:
                shutil.copyfile(output_file_datetime, output_file)
        else:
            shutil.move(output_file_datetime, output_file)

    def _loinc_parent(self, properties, code_map: dict[str, LoincTerm]) -> LoincTerm:

        class_types = properties.get(PT.loinc_class_type, None)
        class_type = None
        if class_types:
            class_type_code = f'classtype_{class_types[0]}'
            class_type = code_map.setdefault(class_type_code, LoincTermIntersection(id=_loincify(class_type_code),
                                                                                    label=f'class type {class_types[0]}',
                                                                                    subClassOf=[
                                                                                             LoincTermId(code_map[
                                                                                                                  '__loincs'].id)
                                                                                         ]
                                                                                    ))

        classes = properties.get(PT.loinc_class, None)
        class_part = None
        if classes:
            class_parts = classes[0].split('.')
            url_suffix = None
            for part in class_parts:
                if not class_part:
                    url_suffix = f'class_{part}'

                    class_part = code_map.setdefault(url_suffix, LoincTermIntersection(
                        id=_loincify(urllib.parse.quote(url_suffix))))
                    class_part.subClassOf = [LoincTermId(class_type.id)]
                    continue
                else:
                    url_suffix = f'{url_suffix}.{part}'
                    class_part = code_map.setdefault(url_suffix,
                                                     LoincTermIntersection(
                                                         id=_loincify(urllib.parse.quote(url_suffix)),
                                                         subClassOf=[LoincTermId(class_part.id)]))

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
