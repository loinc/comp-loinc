from enum import StrEnum
import typing as t


# def get_enum_helper(string: str, enum: t.Type[StrEnum]) -> t.Optional[StrEnum]:
#   e: StrEnum
#   for e in enum:
#     value = e.value
#     name = e.name
#     if e.value.lower() == string.lower() or e.value.lower().endswith(string.lower()):
#       return e
