import shutil
import time
import typing as t
from pathlib import Path

import funowl
import linkml_runtime
from funowl import literals
from linkml_owl.dumpers import owl_dumper

import loinclib
from comp_loinc import datamodel


class CompLoincGenerator:
    LOINCS_ANNOTATIONS = 'loincs-annotations'
    LOINCS_PARTS_EQUIVALENCE = 'loincs-parts-equivalence'

    PARTS_LIST = 'parts-list'
    PARTS_TREES_HIERARCHY = 'parts-trees'

    def __init__(self, loinc_release: loinclib.LoincRelease,
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

        # def _part(self, loinc_part: loinclib.LoincEntity):

    #     part = self.__parts.get(loinc_part.code, ...)
    #     if part is not ...:
    #         return part
    #
    #     params = {
    #         "id": _loincify(loinc_part.code),
    #         "label": f'{loinc_part.name} ({loinc_part.display})',
    #
    #         "part_number": loinc_part.code,
    #         "part_type": loinc_part.part_type,
    #         "subClassOf": ['owl:Thing']
    #     }
    #
    #     part: t.Optional[datamodel.PartClass] = None
    #
    #     # match not available in 3.8
    #     part_classes = {
    #         'TIME': datamodel.TimeClass,
    #         'METHOD': datamodel.MethodClass,
    #         'COMPONENT': datamodel.ComponentClass,
    #         'PROPERTY': datamodel.PropertyClass,
    #         'SYSTEM': datamodel.SystemClass,
    #         'SCALE': datamodel.ScaleClass
    #     }
    #
    #     part = part_classes.get(loinc_part.part_type, datamodel.PartClass)(**params)
    #     self.__parts[loinc_part.code] = part
    #     return part

    # def _part_parents(self, loinc_part: loinclib.LoincEntity,
    #                   parents: t.Dict[str, t.Optional[datamodel.PartClass]] = None) \
    #         -> t.Dict[str, t.Optional[datamodel.PartClass]]:
    #
    #     """
    #     This finds the parents of a LoincEntity by considering if their type is modeled in CompLOINC.
    #
    #     If a parent type is not modeled, the parent's parents are considered recursively. If one of the resolved
    #     parents does not have any parents, None is added to the set as an indicator that the child needs to be a
    #     subclass of owl:Thing.  The lack of None in the set means that the child should not inherit from owl:Thing
    #     """
    #
    #     if parents is None:
    #         parents = {}
    #
    #     # if no parents, we inherit Thing and return
    #     if not loinc_part.parents:
    #         parents['owl:Thing'] = None
    #         return parents
    #
    #     # we have actual parents. But, we're not sure if their type is modeled in CompLOINC
    #     loinc_parent: loinclib.LoincEntity
    #     for loinc_parent in loinc_part.parents:
    #         parent = self._part(loinc_parent)
    #         if parent:
    #             parents[parent.id] = parent
    #         else:
    #             # This parent is not yet modeled in CompLOINC. We try to find a modeled ancestor, or owl:Thing
    #             self._part_parents(loinc_parent, parents)
    #
    #     return parents

    # def generate_parts_ontology(self, add_childless: bool = False):
    #
    #     for loinc_part in self.loinc_release.parts().values():
    #         part = self._part(loinc_part)
    #         if part:  # i.e. we do model this LOINC part in CompLOINC
    #             parents = self._part_parents(loinc_part)
    #             if 'owl:Thing' not in parents:
    #                 part.subClassOf = []
    #             else:
    #                 pass
    #             for parent in parents.values():
    #                 if parent is None:
    #                     continue
    #                 part.subClassOf.append(parent.id)
    #
    #     output_file = self.output_directory / 'parts.owl'
    #     output_file.parent.mkdir(parents=True, exist_ok=True)
    #     print("\n" + f"Writing Part Ontology to output {output_file}")
    #
    #     with open(output_file, 'w') as ccl_owl:  # ./data/output/owl_component_files/part_ontology.owl
    #         all_values = list(self.__parts.values())
    #         actual_values = [x for x in all_values if x is not None]
    #         ccl_owl.write(self._owl_dumper.dumps(actual_values,
    #                                              schema=linkml_runtime.SchemaView(
    #                                                  self.schema_dir / 'part_schema.yaml').schema, ))
    #     print(
    #         "\n" + f"Finished writing Part Ontology to output {output_file} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    # def generate_parts_ontology_3(self):
    #     parts = self.loinc_release.parts().values()
    #
    #     code_part_map: t.Dict[loinclib.LoincEntity, datamodel.PartClass] = {}
    #
    #     part: loinclib.LoincEntity
    #     for part in parts:
    #         params = {
    #             "id": _loincify(part.code),
    #             "label": part.display,
    #
    #             "part_number": part.code,
    #             "part_type": part.part_type,
    #             "subClassOf": [_loincify(c.code) for c in part.parents] if part.parents else ['owl:Thing']
    #             # "subClassOf": [_loincify(c.code) for c in part.parents] if part.parents else ['loinc:FlatPartRoot']
    #         }
    #
    #         code_part_map[part] = datamodel.PartClass(**params)
    #
    #     entity: loinclib.LoincEntity = None
    #     part: datamodel.PartClass = None
    #
    #     hierarchical_parts = [part for entity, part in code_part_map.items() if len(entity.parents) > 0 or len(
    #         entity.children) > 0]
    #     flat_parts = [part for entity, part in code_part_map.items() if len(entity.parents) == 0 and len(
    #         entity.children) == 0]
    #
    #     flat_root = loinclib.LoincEntity('FlatPartRoot')
    #     flat_root.display = '{Flat Part Root}'
    #     flat_root_class = datamodel.PartClass(id=_loincify(flat_root.code), label=flat_root.display,
    #                                           part_number=flat_root.code, subClassOf=['owl:Thing'])
    #     code_part_map[flat_root] = flat_root_class
    #
    #     for flat_part in flat_parts:
    #         flat_part.subClassOf = ['loinc:FlatPartRoot']

    # output_file = self.output_directory / 'parts-all.owl'
    # output_file.parent.mkdir(parents=True, exist_ok=True)
    # print(f'Writing: {output_file}', flush=True)
    # with open(output_file, 'w') as f:
    #     f.write(self._owl_dumper.dumps(list(code_part_map.values()),
    #                                    schema=linkml_runtime.SchemaView(
    #                                        self.schema_dir / 'part_schema.yaml').schema, ))

    def generate_loincs(self):

        loinc_node_ids = self.release.node_ids_for_type(loinclib.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        loincs_root = datamodel.LoincCodeClass(id=_loincify('__loincs'))
        loinc_code_map['__loincs'] = loincs_root

        for loinc_node_id in loinc_node_ids:
            code = loinclib.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc_properties = self.release.node_properties(loinc_node_id)
            attributes = {'id': _loincify(code), 'subClassOf': [loincs_root.id]}

            displays = loinc_properties.get(loinclib.NodeAttributeKey.display, None)
            if displays:
                attributes['label'] = displays[0]
                # attributes['formal_name'] = displays[0]

            definitions = loinc_properties.get(loinclib.NodeAttributeKey.definition, None)
            if definitions:
                definition = definitions[0]
                if literals.Literal._to_n3(definition):
                    # This is needed to work around some unusual string values that throw an error during dumping of:
                    # ./LoincTable/Loinc.csv line: 47536:
                    # "51947-0","Package label.Bottom panel",....
                    attributes['description'] = definition

            loinc = datamodel.LoincCodeClass(**attributes)

            loinc_code_map[code] = loinc

        self._outputs[CompLoincGenerator.LOINCS_ANNOTATIONS] = loinc_code_map
        self._outputs_schema[CompLoincGenerator.LOINCS_ANNOTATIONS] = linkml_runtime.SchemaView(
            self.schema_dir / 'code_schema.yaml')

    def save_outputs(self):
        for filename, output in self._outputs.items():
            self._write_outputs(output_name=filename)

    def generate_loinc_defs(self):

        loinc_node_ids = self.release.node_ids_for_type(loinclib.NodeType.loinc_code)
        loinc_code_map: dict[str, datamodel.LoincCodeClass] = {}

        for loinc_node_id in loinc_node_ids:
            code = loinclib.NodeType.loinc_code.identifier_of_node_id(loinc_node_id)
            loinc = datamodel.LoincCodeClass(id=_loincify(code))
            loinc_code_map[code] = loinc

            # component
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_COMPONENT)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has multiple components: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_component = datamodel.PartClassId(_loincify(part_code))

            # property
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_PROPERTY)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple properties: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_property = datamodel.PartClassId(_loincify(part_code))

            # time
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_TIME)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple times: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_time = datamodel.PartClassId(_loincify(part_code))

            # system
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_SYSTEM)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple systems: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_system = datamodel.PartClassId(_loincify(part_code))

            # scale
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_SCALE)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple scales: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_scale = datamodel.PartClassId(_loincify(part_code))

            # method
            parts = self.release.out_node_ids(loinc_node_id, loinclib.LoincPrimaryEdgeType.Primary_METHOD)
            if len(parts) > 1:
                raise ValueError(f'Loinc: {code} has has multiple methods: {parts}')
            for key, part_node_id in parts.items():
                part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
                loinc.has_method = datamodel.PartClassId(_loincify(part_code))

        self._write_outputs(entities=list(loinc_code_map.values()),
                            schema_file_name='code_schema.yaml',
                            output_name='loinc-defs',
                            ontology_iri='https://loinc.org/code-defs')

    def generate_parts(self):
        part_node_ids = self.release.node_ids_for_type(loinclib.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        # parts_root = datamodel.PartClass(id=_loincify('__parts'))
        # code_part_map['__parts'] = parts_root

        for part_node_id in part_node_ids:
            code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)
            properties: dict = self.release.node_properties(part_node_id)
            part_name = properties.get(loinclib.NodeAttributeKey.part_name, [None])[0]
            part_display_name = properties.get(loinclib.NodeAttributeKey.part_display_name, [None])[0]
            part_type = properties.get(loinclib.NodeAttributeKey.part_type, [None])[0]

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

        part_node_ids = self.release.node_ids_for_type(loinclib.NodeType.loinc_part)
        code_part_map: t.Dict[str, datamodel.PartClass] = {}

        parts_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_trees_hierarchy_root'))
        parts_no_hierarchy_root = datamodel.PartClass(id=_loincify('__parts_no_hierarchy_root'))

        code_part_map['__parts_trees'] = parts_hierarchy_root
        code_part_map['__parts_no_hierarchy'] = parts_no_hierarchy_root

        for part_node_id in part_node_ids:
            part_code = loinclib.NodeType.loinc_part.identifier_of_node_id(part_node_id)

            part = datamodel.PartClass(id=_loincify(part_code))
            parent_ids = self.release.out_node_ids(part_node_id, loinclib.EdgeType.LoincLib_HasParent)
            if parent_ids:
                part.subClassOf = [_loincify(loinclib.NodeType.loinc_part.identifier_of_node_id(parent_id)) for
                                    parent_id in parent_ids.values()]
            else:
                part_parent = None
                child_node_ids = self.release.in_node_ids(part_node_id, loinclib.EdgeType.LoincLib_HasParent)
                for _, child_of_child_node_id in child_node_ids.items():
                    child_node_type = loinclib.NodeType.type_for_node_id(child_of_child_node_id)
                    if child_node_type and child_node_type == loinclib.NodeType.loinc_part:
                        part_parent = parts_hierarchy_root
                        break

                if not part_parent:
                    part_parent = parts_no_hierarchy_root
                part.subClassOf.append(part_parent)
            code_part_map[part_code] = part

        self._outputs[CompLoincGenerator.PARTS_TREES_HIERARCHY] = code_part_map
        self._outputs_schema[CompLoincGenerator.PARTS_TREES_HIERARCHY] = linkml_runtime.SchemaView(
            self.schema_dir / 'part_schema.yaml')

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


def _loincify(id):
    """
    adds the loinc: prefix to loinc part and code numbers
    :param id:
    :return: string
    """
    if id == 'owl:Thing':
        return id

    return f"loinc:{id}"
