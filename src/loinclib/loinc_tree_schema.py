"""Schema for LOINC hierarchy"""

from dataclasses import dataclass

from loinclib import EdgeType, PropertyType, EdgeTypeArgs, PropertyTypeArgs


@dataclass(kw_only=True)
class LoincEdges2Args(EdgeTypeArgs):
  pass


# todo: se: merge with other enum
class LoincEdges(EdgeType):
  """Superclass for all edges from LOINC"""


@dataclass(kw_only=True)
class LoincTreeEdgesArgs(LoincEdges2Args):
  pass


class LoincTreeEdges(LoincEdges):
  """Edges from the LOINC tree browser."""

  tree_parent = LoincTreeEdgesArgs(name="tree_parent")

@dataclass(kw_only=True)
class LoincDanglingNlpEdgesArgs(LoincEdges2Args):
  pass

class LoincDanglingNlpEdges(LoincEdges):
  """Edges from  NLP process to connect dangling parts into the hierarchy."""

  nlp_parent = LoincDanglingNlpEdgesArgs(name="nlp_parent")

@dataclass(kw_only=True)
class LoincTreePropsArgs(PropertyTypeArgs):
  pass

class LoincTreeProps(PropertyType):
  """Properties of a LOINC tree browser."""

  code_text = LoincTreePropsArgs(name="code_text")
  from_trees = LoincTreePropsArgs(name="from_trees")
  from_trees_component_by_system = LoincTreePropsArgs(name="is_tree_component_by_system")
