"""Schema for LOINC hierarchy"""
from enum import StrEnum

class LoincEdges(StrEnum):
    """Superclass for all edges from LOINC"""
    pass

class LoincTreeEdges(LoincEdges):
    """Edges from the LOINC tree browser."""
    tree_parent = "tree_parent"

class LoincDanglingNlpEdges(LoincEdges):
    """Edges from  NLP process to connect dangling parts into the hierarchy."""
    nlp_parent = "nlp_parent"

class LoincTreeProps(StrEnum):
    """Properties of a LOINC tree browser."""
    code_text = "code_text"
    from_trees = "from_trees"
