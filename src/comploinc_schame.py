from dataclasses import dataclass

from loinclib import NodeType, NodeTypeArgs


@dataclass(kw_only=True)
class ComploincNodeTypeArgs(NodeTypeArgs):
  pass

class ComploincNodeType(NodeType):
  root_node = ComploincNodeTypeArgs(name="root_node", id_prefix="comploinc")
  group_node = ComploincNodeTypeArgs(name="group_node", id_prefix="comploinc")