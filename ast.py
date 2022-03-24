from typing import Union
from unicodedata import name
from type import *
from symbolTable import SymbolTable
from tac import *

RootType = 'Root'
FunctionDefType = 'FunctionDef'
StatementListType = 'StatementList'
IfStatementType = 'IfStatement'
WhileStatementType = 'WhileStatement'
ForStatementType = 'ForStatement'
DefineListType = 'DefineList'
DefineType = 'Define'
ArgDefineListType = 'ArgDefineList'
FunctionCallType = 'FunctionCall'
FunctionCallArgListType = 'FunctionCallArgList'
FunctionReturnType = 'FunctionReturn'

class Context:
    def __init__(self,symbols,globalFns,fnName) -> None:
        self.symbols:SymbolTable = symbols
        self.globalFns:dict[str,GlobalFunction] = globalFns
        self.fnName: str = fnName

varCnt = 0

def clear():
    global varCnt
    varCnt = 0


class NodeVisitorReturn:
    def __init__(self,code,dst  =None) -> None:
        self.code:list[ThreeAddressCode] = code
        self.dst:Union[VariableCode , LiteralCode] = dst
    
class BasicASTNode:
    def __init__(self,type) -> None:
        self.type = type
    def visit(self,context:Context):
        pass

class FunctionASTNode(BasicASTNode):
    def __init__(self, name,args,returnType,statements) -> None:
        super().__init__(FunctionDef)
        self.name = name
        self.args = args
        self.returnType = returnType
        self.statements = []
        for it in statements.statements:
            self.statements.append(it)
        self.haveReturn = statements.haveReturn
    def getArgsType():
        pass
    
class RootASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(RootType)
        self.fns:list[FunctionASTNode] = []
        self.main = None
    def merge(self,other):
        for it in other.fns:
            self.fns.append(it)
        if other.main is not None:
            self.main = other.main
    def visit(self,context: Context):
        if self.main is not None:
            raise Error('main function is not defined')
        context.globalFns[Main] = GlobalFunction(
            type=voidType,
            args=self.main.getArgsType(),
            address=1,
            memCount=0,
            name=Main
        )
        for fn in self.fns:
            context.globalFns[fn.name] = GlobalFunction(
                type = fn.returnType,
                args = fn.getArgsType(),
                address = -1,
                memCount = 0,
                name= fn.name
            )
        start = FunctionCallCode(
            type=ThreeAddressCodeType.FunctionCall,
            name=Main
        )
        code:list[ThreeAddressCode] = [start]
        code += self.main.visit(context).code
        context.globalFns[Main].memCount = varCnt
        for fn in self.fns:
            context.fnName = fn.name
            varCnt = 0
            code.append(ThreeAddressCodeType.NOP)
            res = fn.visit(context)
            fnObj = context.globalFns[fn.name]
            fnObj.address = len(code)
            fnObj.memCount = varCnt
            code += res.code
        return code
