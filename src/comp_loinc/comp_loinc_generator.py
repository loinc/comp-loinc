import pathlib
import typing
from datetime import datetime

import linkml_runtime
from linkml_owl.dumpers import owl_dumper

import loinclib
from comp_loinc import datamodel


class CompLoincGenerator:

    def __init__(self, loinc_release: loinclib.LoincRelease,
                 schema_directory: pathlib.Path,
                 output_directory: pathlib.Path):
        self.loinc_release = loinc_release
        self.schema_dir = schema_directory
        self.output_directory = output_directory

        self.__od = owl_dumper.OWLDumper()
        self.__parts: typing.Dict[str, datamodel.PartClass] = {}

    def _part(self, loinc_part: loinclib.LoincEntity):
        part = self.__parts.get(loinc_part.code, ...)
        if part is not ...:
            return part

        params = {
            "id": _loincify(loinc_part.code),
            "part_number": loinc_part.code,
            "label": f'{loinc_part.part_name} ({loinc_part.part_display})',
            "part_type": loinc_part.part_type,
            "subClassOf": ['owl:Thing']
        }

        part: typing.Optional[datamodel.PartClass] = None
        match loinc_part.part_type:
            case "TIME":
                part = datamodel.TimeClass(**params)
            case "METHOD":
                part = datamodel.MethodClass(**params)
            case "COMPONENT":
                part = datamodel.ComponentClass(**params)
            case "CLASS":
                # Some components are of part type CLASS (I thought this was only for abstract classes)
                part = datamodel.ComponentClass(**params)
            case "PROPERTY":
                part = datamodel.PropertyClass(**params)
            case "SYSTEM":
                part = datamodel.SystemClass(**params)
            case "SCALE":
                part = datamodel.ScaleClass(**params)

        self.__parts[loinc_part.code] = part
        return part

    def _part_parents(self, loinc_part: loinclib.LoincEntity,
                      parents: typing.Dict[str, typing.Optional[datamodel.PartClass]] = None) \
            -> typing.Dict[str, typing.Optional[datamodel.PartClass]]:

        """
        This finds the parents of a LoincEntity by considering if their type is modeled in CompLOINC.

        If a parent type is not modeled, the parent's parents are considered recursively. If one of the resolved
        parents does not have any parents, None is added to the set as an indicator that the child needs to be a
        subclass of owl:Thing.  The lack of None in the set means that the child should not inherit from owl:Thing
        """

        if parents is None:
            parents = {}

        # if no parents, we inherit Thing and return
        if not loinc_part.parents:
            parents['owl:Thing'] = None
            return parents

        # we have actual parents. But, we're not sure if their type is modeled in CompLOINC
        loinc_parent: loinclib.LoincEntity
        for loinc_parent in loinc_part.parents:
            parent = self._part(loinc_parent)
            if parent:
                parents[parent.id] = parent
            else:
                # This parent is not yet modeled in CompLOINC. We try to find a modeled ancestor, or owl:Thing
                self._part_parents(loinc_parent, parents)

        return parents

    def generate_parts_ontology(self, add_childless: bool = False):

        for loinc_part in self.loinc_release.parts().values():
            part = self._part(loinc_part)
            if part:  # i.e. we do model this LOINC part in CompLOINC
                parents = self._part_parents(loinc_part)
                if 'owl:Thing' not in parents:
                    part.subClassOf = []
                else:
                    pass
                for parent in parents.values():
                    if parent is None:
                        continue
                    part.subClassOf.append(parent.id)

        output_file = self.output_directory / 'parts.owl'
        output_file.parent.mkdir(parents=True, exist_ok=True)
        print("\n" + f"Writing Part Ontology to output {output_file}")

        with open(output_file, 'w') as ccl_owl:  # ./data/output/owl_component_files/part_ontology.owl
            all_values = list(self.__parts.values())
            actual_values = [x for x in all_values if x is not None]
            ccl_owl.write(self.__od.dumps(actual_values,
                                          schema=linkml_runtime.SchemaView(
                                              self.schema_dir / 'part_schema.yaml').schema, ))
        print(
            "\n" + f"Finished writing Part Ontology to output {output_file} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")


def _loincify(id):
    """
    adds the loinc: prefix to loinc part and code numbers
    :param id:
    :return: string
    """
    if id == 'owl:Thing':
        return id

    return f"loinc:{id}"
