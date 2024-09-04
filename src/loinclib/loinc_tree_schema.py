from enum import StrEnum


class LoincTreeEdges(StrEnum):
  tree_parent = 'tree_parent'

class LoincTreeProps(StrEnum):
  code_text = 'code_text'
  from_trees = 'from_trees'