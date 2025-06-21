from dataclasses import dataclass
from enum import Enum


# https://stackoverflow.com/questions/26691784/can-named-arguments-be-used-with-python-enums#answer-52604491


@dataclass(kw_only=True)
class SchemaTypeArgs:
    id_prefix: str


class SchemaType(Enum):
    pass

    # def __new__(cls, *args, **kwargs):
    #   print("Base Enum new called")
    #   obj = object.__new__(cls)
    #   obj._value_ = args[0]
    #   return obj

    def __init__(self, args: SchemaTypeArgs, **kwargs):
        print("base inited")
        self.id_prefix = args.id_prefix


@dataclass(kw_only=True)
class NodeTypeArgs(SchemaTypeArgs):
    node_prefix: str


class NodeType(SchemaType):
    FOO = NodeTypeArgs(node_prefix="FOO_PREFIX", id_prefix="FOO_ID_PREFIX")

    # def __new__(cls, *args, **kwargs):
    #   print("Enum new called")
    #   obj = object.__new__(cls)
    #   obj._value_ = args[0]
    #   return obj

    def __init__(self, args: NodeTypeArgs, **kwargs):
        super().__init__(args, **kwargs)
        print(" inited")
        self.node_prefix = args.node_prefix


print(NodeType.FOO.id_prefix)
print(NodeType.FOO.node_prefix)
