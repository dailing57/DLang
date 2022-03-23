class Variable:
    def __init__(self, id, name, isArg, isConst, isGlobal, type=None, value=None) -> None:
        self.id = id
        self.name = name
        self.isArg = isArg
        self.isConst = isConst
        self.isGloabal = isGlobal
        self.type = type
        self.value = value


class Literal:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value


class UserFunction:
    def __init__(self, type, args, address, memCount, name) -> None:
        self.type = type
        self.args = args
        self.address = address
        self.memCount = memCount
        self.name = name


class BuiltinFunction:
    def __init__(self, type, args, fn, name) -> None:
        self.type = type
        self.args = args
        self.fn = fn
        self.name = name

class Error(Exception):
    def __init__(self, message=None):
        self.message = f'{self.__class__.__name__}: {message}'

stringType = 'stringType'
numberType = 'numberType'
floatType = 'floatType'
boolType = 'boolType'
voidType = 'voidType'

