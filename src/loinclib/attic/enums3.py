from dataclasses import dataclass
from enum import StrEnum


@dataclass(kw_only=True)
class TypeArgs:
  name: str
  entity_id: str


class Type(StrEnum):
  def __new__(cls, *args, **kwargs):
    print("debug")
    obj = str.__new__(cls)
    obj._value_ = args[0]
    return obj

  def __init__(self, name, args):
    print("debug")
    self.args = args


@dataclass(kw_only=True)
class EntityTypeArgs(TypeArgs):
  entity_id: str


class EntityType(Type):
  def __new__(cls, *args, **kwargs):
    print("debug")
    obj = str.__new__(cls)
    obj._value_ = args[0]
    return obj

  def __init__(self, name, args):
    super().__init__(name, args)
    print("debug")


class MyEntities(EntityType):
  E1 = "some name", EntityTypeArgs(name="some name", entity_id="some_entity_id")


a = MyEntities.E1

print(MyEntities.E1.value)
print(MyEntities.E1.args)
