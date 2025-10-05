"""LOINC-SNOMED Ontology schema"""

from dataclasses import dataclass

from loinclib import EdgeType, EdgeTypeArgs

@dataclass(kw_only=True)
class LoincSnomedEdgesArgs(EdgeTypeArgs):
    pass


class LoincSnomedEdges(EdgeType):
    """Edges for the LOINC-SNOMED ontology"""
    loinc_term_maps_to = LoincSnomedEdgesArgs(name="loinc_term_maps_to")
    loinc_part_maps_to = LoincSnomedEdgesArgs(name="loinc_part_maps_to")

