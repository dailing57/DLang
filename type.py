from typing import Union
from lex_zh import *

FunctionDef = 'FunctionDef'
globalAddress = 'globalAddress'
VariableType = 'Variable'
LiteralType = 'Literal'


class Variable:
    def __init__(self, id, name, isArg=False, isConst=True, isGlobal=False, type=None, value=None) -> None:
        self.id = id
        self.name = name
        self.isArg = isArg
        self.isConst = isConst
        self.isGloabal = isGlobal
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class Literal:
    def __init__(self, type, value) -> None:
        self.type = type
        self.value = value

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class UserFunction:
    def __init__(self, type, args, address, memCount, name) -> None:
        self.type = type
        self.args = args
        self.address = address
        self.memCount = memCount
        self.name = name

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class BuiltinFunction:
    def __init__(self, type, args, fn, name) -> None:
        self.type = type
        self.args = args
        self.fn = fn
        self.name = name


class Error(Exception):
    def __init__(self, message=None):
        self.message = f'{self.__class__.__name__}: {message}'


GlobalFunction = Union[UserFunction, BuiltinFunction]
