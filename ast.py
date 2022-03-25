from typing import Union
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
    def __init__(self,code,dst=None) -> None:
        self.code:list[ThreeAddressCode] = code
        self.dst:Union[VariableCode , LiteralCode] = dst
    
class BasicASTNode:
    def __init__(self,type) -> None:
        self.type = type
    def visit(self,context:Context) -> NodeVisitorReturn:
        pass

class BinOPASTNode(BasicASTNode):
    def __init__(self,type,dst,x,y) -> None:
        super().__init__(type)
        self.dst:Variable = dst
        self.x:ValueASTNode = x
        self.y:ValueASTNode = y
    def visit(self, context: Context):
        code:list[ThreeAddressCode] = []
        xres = self.x.visit(context=context)
        yres = self.y.visit(context=context)
        if xres.dst is not None and yres.dst is not None:
            code += xres.code
            if globalAddress in xres.dst and xres.dst.globalAddress == 0:
                global varCnt
                varCnt+=1
                tmpDst = LocalVariableCode(varCnt,type=xres.dst.type)
                context.symbols.add(tmpDst.address,'$'+str(tmpDst.address),tmpDst.type)
                assignCode = UnitOPCode(
                    type = Assign,
                    dst = tmpDst,
                    src = xres.dst
                )
                code.append(assignCode)
                xres.dst = tmpDst
            varCnt+=1
            tmpVar = varCnt
            type = getBinOPType(self.type,xres.dst.type,yres.dst.type)
            if type is not None:
                context.symbols.add(tmpVar,'$'+str(tmpVar),type)

                if self.type == And or self.type == Or:
                    ifGoto = IfGotoCode(
                        type = ThreeAddressCodeType.IfGoto,
                        src=xres.dst,
                        target=(self.type == And),
                        offset = 2 
                    )
                    code.append(ifGoto)
                    code.append(UnitOPCode(
                        type=Assign,
                        dst=LocalVariableCode(address=tmpVar,type=type),
                        src=LiteralCode(value=(self.type==Or),type=boolType)
                    ))
                    code.append(GotoCode(
                        type=ThreeAddressCodeType.Goto,
                        offset=len(yres.code) + 1
                    ))
                code += yres.code
                code.append(BinOPCode(
                    type=self.type,
                    dst=LocalVariableCode(address=tmpVar,type=type),
                    x=xres.dst,
                    y=yres.dst
                ))
                return NodeVisitorReturn(code=code,dst=LocalVariableCode(address=tmpVar,type=type))
            else:
                raise Error('Type Error')
        else:
            raise Error('unknown')

class UnitASTNode(BasicASTNode):
    pass

class LeafASTNode(BasicASTNode):
    pass

class FunctionCallASTNode(BasicASTNode):
    pass

ValueASTNode = Union[BinOPASTNode,UnitASTNode,LeafASTNode,FunctionCallASTNode]

class RootASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(RootType)
        self.fns:list[FunctionASTNode] = []
        self.main:FunctionASTNode = None
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
        global varCnt
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
        return NodeVisitorReturn(code)


class ArgDefineListASTNode(BasicASTNode):
    def __init__(self, type) -> None:
        super().__init__(ArgDefineListType)
        self.defs:list[Variable] = []
    
    def merge(self, other):
        self.defs += other.defs

    def visit(self, context: Context):
        for i in range(len(self.defs)):
            d = self.defs[i]
            context.symbols.add(Variable(
                id= i - len(self.defs),
                name=d.name,
                type = d.type,
                isArg=True,
                isConst=False
            ))
        return super().visit(context)

class StatementListASTNode(BasicASTNode):
    def __init__(self, createContext = False) -> None:
        super().__init__(StatementListType)
        self.createContext = createContext
        self.statements:list[Sta]

class FunctionReturnASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(FunctionReturnType)
        self.src = ValueASTNode

class FunctionASTNode(BasicASTNode):
    def __init__(self, name,args,returnType,statements) -> None:
        super().__init__(FunctionDef)
        self.name = name
        self.args: ArgDefineListASTNode = args
        self.returnType = returnType
        self.statements: list[StatementListASTNode] = []
        for it in statements.statements:
            self.statements.append(it)
        self.haveReturn = statements.haveReturn
    def getArgsType(self):
        pass


