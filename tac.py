from type import *
from typing import Union


class GlobalVariableCode:
    def __init__(self, globalAddress, type) -> None:
        self.globalAddress = globalAddress
        self.type = type

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class LocalVariableCode:
    def __init__(self, address, type) -> None:
        self.address = address
        self.type = type

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


VariableCode = Union[GlobalVariableCode, LocalVariableCode]


class ThreeAddressCodeType:
    NOP = 'NOP'
    FunctionCall = 'FunctionCall'
    FunctionReturn = 'FunctionReturn'
    FunctionCreate = 'FunctionCreate'
    Goto = 'Goto'
    IfGoto = 'IfGoto'
    Plus = 'Plus'
    Minus = 'Minus'
    Mul = 'Mul'
    Div = 'Div'
    Mod = 'Mod'
    Negative = 'Negative'
    Not = 'Not'
    And = 'And'
    Or = 'Or'
    NotEqual = 'NotEqual'
    Equal = 'Equal'
    LessThan = 'LessThan'
    MoreThan = 'MoreThan'
    LessOrEqual = 'LessOrEqual'
    MoreOrEqual = 'MoreOrEqual'
    Assign = 'Assign'
    PushStack = 'PushStack'


NOPCodeType = ThreeAddressCodeType.NOP
FunctionCallCodeType = ThreeAddressCodeType.FunctionCall
FunctionReturnCodeType = ThreeAddressCodeType.FunctionReturn
GotoCodeType = ThreeAddressCodeType.Goto
IfGotoCodeType = ThreeAddressCodeType.IfGoto


class NOPCode:
    def __init__(self, type) -> None:
        self.type = type

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class FunctionCallCode:
    def __init__(self, type, name) -> None:
        self.type = type
        self.name = name

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class FunctionReturnCode:
    def __init__(self, type, name, src=None) -> None:
        self.type = type
        self.name = name
        self.src = src

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class GotoCode:
    def __init__(self, type, offset) -> None:
        self.type = type
        self.offset = offset

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class IfGotoCode:
    def __init__(self, type, src, target, offset) -> None:
        self.type = type
        self.src = src
        self.target = target
        self.offset = offset

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class LiteralCode:
    def __init__(self, value, type) -> None:
        self.value = value
        self.type = type

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class BinOPCode:
    def __init__(self, type, dst, x, y) -> None:
        self.type = type
        self.dst = dst
        self.x: Union[VariableCode, LiteralCode] = x
        self.y: Union[VariableCode, LiteralCode] = y

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class UnitOPCode:
    def __init__(self, type, dst, src) -> None:
        self.type = type
        self.dst = dst
        self.src = src

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class PushStackCode:
    def __init__(self, type, src) -> None:
        self.type = type
        self.src = src

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


class CreateFunction:
    def __init__(self, funAddress, catchList) -> None:
        self.funAddress = funAddress
        self.catchList = catchList

    def __str__(self) -> str:
        return ' '.join(('%s' % item for item in self.__dict__.values()))


ThreeAddressCode = Union[
    NOPCode,
    FunctionCallCode,
    FunctionReturnCode,
    GotoCode,
    IfGotoCode,
    BinOPCode,
    UnitOPCode,
    PushStackCode,
    CreateFunction
]


def getBinOPType(op, a=None, b=None):
    if a is None or b is None:
        return None
    if a == voidType or b == voidType:
        return None
    if op == ThreeAddressCodeType.Plus:
        if a == stringType or b == stringType:
            return stringType
        elif a == complexType or b == complexType:
            return complexType
        elif a == floatType or b == floatType:
            return floatType
        else:
            return numberType
    elif op == ThreeAddressCodeType.Minus:
        if a == stringType or b == stringType:
            return None
        elif a == complexType or b == complexType:
            return complexType
        elif a == floatType or b == floatType:
            return floatType
        else:
            return numberType
    elif op == ThreeAddressCodeType.Mul:
        if a == stringType or b == stringType:
            return None
        elif a == complexType or b == complexType:
            return complexType
        elif a == floatType or b == floatType:
            return floatType
        else:
            return numberType
    elif op == ThreeAddressCodeType.Div:
        if a == stringType or b == stringType:
            return None
        elif a == complexType or b == complexType:
            return complexType
        elif a == floatType or b == floatType:
            return floatType
        else:
            return numberType
    elif op == ThreeAddressCodeType.Mod:
        if a == stringType or b == stringType:
            return None
        elif a == floatType or b == floatType:
            return floatType
        else:
            return numberType
    elif op == ThreeAddressCodeType.And or op == ThreeAddressCodeType.Or or op == ThreeAddressCodeType.Equal or op == ThreeAddressCodeType.NotEqual or op == ThreeAddressCodeType.LessOrEqual or op == ThreeAddressCodeType.LessThan or op == ThreeAddressCodeType.MoreOrEqual or op == ThreeAddressCodeType.MoreThan:
        return boolType
    else:
        return None


def getUnitOPType(op, src):
    if src is None:
        return None
    if src == voidType:
        return None
    if op == ThreeAddressCodeType.Assign:
        return src
    elif op == ThreeAddressCodeType.Negative:
        if src == stringType:
            return None
        return src
    elif op == ThreeAddressCodeType.Not:
        return boolType
    else:
        return None
