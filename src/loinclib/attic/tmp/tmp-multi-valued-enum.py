import enum

from comp_loinc.datamodel.comp_loinc import LoincPart


class MultiValuedEnum(enum.Enum):
    ONE = {"one": "1"}

    def __new__(cls, *args, **kwds):
        value = len(cls.__members__) + 1
        obj = object.__new__(cls)
        obj._value_ = value
        return obj

    def __init__(self,
                 data):
        self.data = data


if __name__ == '__main__':
    print(MultiValuedEnum.ONE)
    print(MultiValuedEnum.ONE.data['one'])
    part = LoincPart()
    print(part)
