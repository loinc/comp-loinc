from enum import StrEnum


class SomeEnum(StrEnum):
  One = 'one'



print(f'Enum name: {SomeEnum.One.name}')
print(f'Enum value: {SomeEnum.One.value}')
print(f'Enum print value: {SomeEnum.One}')


a = SomeEnum.One

print(repr(a))


a2 = SomeEnum('one')

print(a2)

