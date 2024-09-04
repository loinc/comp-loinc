import dataclasses


@dataclasses.dataclass
class Test:
    f1: str = None


test = Test()

print(test)


class T2:

    def __setitem__(self, key, value):
        print(f'setitem Key: {key} and value {value}')

    def __setattr__(self, key, value):
        print(f'setattr Key: {key} and value {value}')


t2 = T2()
t2.a = "A"

