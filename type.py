from typing import Union
# ValueType

stringType  = 'stringType'
numberType  = 'numberType'
floatType   = 'floatType'
boolType    = 'boolType'
voidType    = 'voidType'

# CmpOPType
NotEqual    = 'NotEqual'
Equal       = 'Equal'
LessThan    = 'LessThan'
MoreThan    = 'MoreThan'
LessOrEqual = 'LessOrEqual'
MoreOrEqual = 'MoreOrEqual'

# BinOPType
Plus        = 'Plus'
Minus       = 'Minus'
Mul         = 'Mul'
Div         = 'Div'
Mod         = 'Mod'
Negative    = 'Negative'
Not         = 'Not'
And         = 'And'
Or          = 'Or'

# UnitOPType
Negative    = 'Negative'
Not         = 'Not'
Assign      = 'Assign'

# VoidType
VoidType    = 'voidType'

Main        = 'main'
FunctionDef = 'FunctionDef'
globalAddress = 'globalAddress'
VariableType = 'Variable'
LiteralType  = 'Literal'
class Variable:
    def __init__(self, id, name, isArg=False, isConst=True, isGlobal=False, type=None, value=None) -> None:
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

GlobalFunction = Union[UserFunction , BuiltinFunction]
