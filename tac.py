from enum import Enum


class GlobalVariavleCode:
    def __init__(self,globalAddress,type) -> None:
        self.globalAddress = globalAddress
        self.type = type

class LocalVariableCode:
    def __init__(self,address,type) -> None:
        self.addres = address
        self.type = type

class ThreeAddressCodeType(Enum):
    NOP = 'NOP',
    FunctionCall = 'FunctionCall',
    FunctionReturn = 'FunctionReturn',
    Goto = 'Goto',
    IfGoto = 'IfGoto',
    Plus = 'Plus',
    Minus = 'Minus',
    Mul = 'Mul',
    Div = 'Div',
    Mod = 'Mod',
    Negative = 'Negative',
    Not = 'Not',
    And = 'And',
    Or = 'Or',
    NotEqual = 'NotEqual',
    Equal = 'Equal',
    LessThan = 'LessThan',
    MoreThan = 'MoreThan',
    LessOrEqual = 'LessOrEqual',
    MoreOrEqual = 'MoreOrEqual',
    Assign = 'Assign',
    PushStack = 'PushStack'

NOPCodeType = ThreeAddressCodeType.NOP
FunctionCallCodeType = ThreeAddressCodeType.FunctionCall
FunctionReturnCodeType = ThreeAddressCodeType.FunctionReturn
GotoCodeType =  ThreeAddressCodeType.Goto
IfGotoCodeType =  ThreeAddressCodeType.IfGoto

class NOPCode:
    def __init__(self,type) -> None:
        self.type = type

class FunctionCallCode:
    def __init__(self,type,name) -> None:
        self.type = type
        self.name = name

class FunctionReturnCode:
    def __init__(self,type,name,src=None) -> None:
        self.type = type
        self.name = name
        self.src = src

class GotoCode:
    def __init__(self,type,offset) -> None:
        self.type = type
        self.offset = offset