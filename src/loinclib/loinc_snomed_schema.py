"""LOINC-SNOMED Ontology schema"""

from dataclasses import dataclass

from loinclib import EdgeType, EdgeTypeArgs

@dataclass(kw_only=True)
class LoincSnomedEdgesArgs(EdgeTypeArgs):
    pass


class LoincSnomedEdges(EdgeType):
    """Edges for the LOINC-SNOMED ontology"""
    pass


