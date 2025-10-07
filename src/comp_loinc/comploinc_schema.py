from dataclasses import dataclass

from loinclib import NodeType, NodeTypeArgs


@dataclass(kw_only=True)
class ComploincNodeTypeArgs(NodeTypeArgs):
  pass

class ComploincNodeType(NodeType):
  comploinc = ComploincNodeTypeArgs(name="comploinc", id_prefix="comploinc")
  root_node = ComploincNodeTypeArgs(name="root_node", id_prefix="comploinc")
  group_node = ComploincNodeTypeArgs(name="group_node", id_prefix="comploinc")
  groupings = ComploincNodeTypeArgs(name="Groupings", id_prefix="comploinc")
  part_type = ComploincNodeTypeArgs(name="PartType", id_prefix="comploinc_")


