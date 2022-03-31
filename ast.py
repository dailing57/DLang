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

def clearAST():
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
            if hasattr(xres.dst,globalAddress) and xres.dst.globalAddress == 0:
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

class UnitOPASTNode(BasicASTNode):
    def __init__(self, type,dst,src) -> None:
        super().__init__(type)
        self.dst:Variable = dst
        self.src:ValueASTNode = src
    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        res = self.src.visit(context=context)
        if res.dst is not None:
            code += res.code
            if self.dst.id == -1:
                mem = context.symbols.query(self.dst.name)
                if mem is not None:
                    if mem.type is None:
                        mem.type = res.dst.type
                    elif mem.type != res.dst.type:
                        raise Error(f'{mem.type} variable {self.dst.name} can not be assigned {res.dst.type} value')
                    if self.type == Assign and mem.isConst:
                        raise Error(f'const variable {self.dst.name} can not be assigned a new value')
                    dst = GlobalVariableCode(globalAddress=mem.id,type=mem.type) if mem.isGloabal else LocalVariableCode(address=mem.id,type=mem.type)
                    code.append(UnitOPCode(
                        type=self.type,
                        dst = dst,
                        src = res.dst
                    ))
                    return NodeVisitorReturn(code=code,dst=dst)   
                else:
                    raise(Error(f'variable {self.dst.name} is not defined'))
            else:
                global varCnt
                varCnt+=1
                tmpVar = varCnt
                type = getUnitOPType(self.type,res.dst.type)
                if type is not None:
                    context.symbols.add(tmpVar,'$'+str(tmpVar),type)
                    code.append(UnitOPCode(
                        type = self.type,
                        dst = LocalVariableCode(address=tmpVar,type=type),
                        src = res.dst
                    ))
                    return NodeVisitorReturn(code,LocalVariableCode(address=tmpVar,type=type))
                else:
                    raise(Error('Type Error'))
        else:
            raise(Error('unknown'))

class LeafASTNode(BasicASTNode):
    def __init__(self, item) -> None:
        if hasattr(item,'id'):
            VariableType
            super().__init__(VariableType)
        else:
            super.__init__(LiteralType)
        self.dst:Union[Variable,Literal] = item
    def visit(self, context: Context) -> NodeVisitorReturn:
        if self.type == VariableType:
            name = self.dst.name
            mem = context.symbols.query(name)
            if mem is not None:
                if mem.type is not None:
                    dst =GlobalVariableCode(globalAddress=mem.id,type=mem.type) if mem.isGloabal else LocalVariableCode(address=mem.id,type=mem.type)
                    return NodeVisitorReturn([],dst=dst)
                else:
                    raise(Error(f'variable {name} is not in initialized'))
            else:
                raise(Error(f'variable {name} is not defined'))
        elif self.type == LiteralType:
            dst = self.dst
            return NodeVisitorReturn([],dst=LiteralCode(value=dst.value,tyep=dst.type))
        else:
            raise(Error('unknown'))

class FunctionCallArgListASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(FunctionCallArgListType)
        self.args:list[ValueASTNode] = []
        self.types = []

    def merge(self,other):
        self.args += other.args
    
    def checkType(self,realArgs:list):
        if len(self.types) != len(realArgs):
            return False
        for i in range(len(realArgs)):
            if self.types[i] != realArgs[i]:
                return False
        return True
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        for arg in self.args:
            res = arg.visit(context)
            if res.dst is not None:
                self.types.append(res.dst.type)
                code += res.code
                pushCode = PushStackCode(
                    type= ThreeAddressCodeType.PushStack,
                    src= res.dst
                )
                code.append(pushCode)
            else:
                raise(Error('Type Error'))
        return NodeVisitorReturn(code)

class FunctionCallASTNode(BasicASTNode):
    def __init__(self, name, args) -> None:
        super().__init__(FunctionCallType)
        self.name:str = name
        self.args:FunctionCallArgListASTNode = args
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        fn = context.globalFns[self.name]
        if fn is not None:
            if len(self.args) == len(fn.args):
                code:list[ThreeAddressCode] = []
                res = self.args.visit(context=context)
                if self.args.checkType(fn.args):
                    code += res.code
                    callCode:FunctionCallCode(
                        type=ThreeAddressCodeType.FunctionCall,
                        name=self.name
                    )
                    code.append(callCode)
                    if fn.type == voidType:
                        return NodeVisitorReturn(code)
                    else:
                        dst = GlobalVariableCode(globalAddress=0,type = fn.type)
                        return NodeVisitorReturn(code,dst)
                else:
                    raise(Error(f'function "{self.name}" call arg list types are not matched'))
            else:
                raise(Error(f'function "{self.name}" call arg list length is not matched'))
        else:
            raise(Error(f'function "{self.name}" is not defined'))

ValueASTNode = Union[BinOPASTNode,UnitOPASTNode,LeafASTNode,FunctionCallASTNode]

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
        return NodeVisitorReturn([])

class FunctionReturnASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(FunctionReturnType)
        self.src: ValueASTNode = None
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        fnObj = context.globalFns[context.fnName]
        if fnObj is None:
            raise(Error('unknown'))
        if self.src is not None:
            code:list[ThreeAddressCode] = []
            res = self.src.visit(context)
            if res.dst is not None:
                code += res.code
                if fnObj.type != res.dst.type:
                    raise(Error(f'function "${context.fnName}" should return <void>, but return <{res.dst.type}>'))
                returnCode = FunctionReturnCode(
                    type=ThreeAddressCodeType.FunctionReturn,
                    name=context.fnName,
                    src=res.dst
                )
                code += returnCode
                return NodeVisitorReturn(code)
            else:
                raise(Error(f'function "{context.fnName}" return value is void'))
        else:
            if fnObj.type != voidType:
                raise(Error(f'function "{context.fnName}" should return <{fnObj.type}>, but return <void>'))
            returnCode = FunctionReturnCode(
                type= ThreeAddressCodeType.FunctionReturn,
                name = context.fnName
            )
            return NodeVisitorReturn([returnCode])


class DefineASTNode(BasicASTNode):
    def __init__(self,dst,src=None) -> None:
        super().__init__(DefineType)
        self.dst:Variable = dst
        self.src:ValueASTNode = src

    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        if self.src is not None:
            res = self.src.visit(context)
            code += res.code
            if res.dst is not None:
                if self.dst.type == None or self.dst.type == res.dst.type:
                    global varCnt
                    varCnt += 1
                    address = varCnt
                    context.symbols.add(Variable(address,self.dst.name,res.dst.type,isConst=self.dst.isConst))
                    assign = UnitOPCode(
                        type = Assign,
                        dst = LocalVariableCode(
                            address=address,
                            type=res.dst.type
                        )
                    )
                    code.append(assign)
                    return NodeVisitorReturn(code)
                else:
                    raise(Error(f'variable {self.dst.name}\'s type not match'))
            else:
                raise(Error('unknown'))
        else:
            if self.dst.isConst:
                raise(Error(f'const variable {self.dst.name} is not initialized'))    
            varCnt += 1
            context.symbols.add(Variable( id=varCnt,name = self.dst.name,type=self.dst.type,isConst=self.dst.isConst))
            return NodeVisitorReturn([])

class DefineListASTNode(BasicASTNode):
    def __init__(self) -> None:
        super().__init__(DefineListType)
        self.defs:list[DefineASTNode] = []
        self.isConst = False
    
    def merge(self,other):
        self.defs += other.defs
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        for defn in self.defs:
            code += defn.visit(context).code
        return NodeVisitorReturn(code)



class ForStatementASTNode(BasicASTNode):
    def __init__(self, init, condition, update, body) -> None:
        super().__init__(ForStatementType)
        self.init:Union[DefineListASTNode,list[UnitOPASTNode]] = init
        self.condition: ValueASTNode = condition
        self.update: list[UnitOPASTNode] = update
        self.body: StatementASTNode = body
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        sTable = SymbolTable()
        sTable.father = context.symbols
        context = Context(symbols=sTable,globalFns=context.globalFns,fnName=context.fnName)
        code:list[ThreeAddressCode] = []
        if hasattr(self.init,'type'):
            initRes = self.init.visit(context)
            code += initRes.code
        else:
            for assign in self.init:
                assignRes = assign.visit(context)
                code += assignRes
        initLen = len(code)
        condRes = self.condition.visit(context)
        if condRes.dst is not None:
            code += condRes.code
            ifFalseGoto = IfGotoCode(
                type = ThreeAddressCodeType.IfGoto,
                src = condRes.dst,
                offset = len(code),
                target = False
            )
            code.append(ifFalseGoto)
            bodyRes = self.body.visit(context)
            code += bodyRes.code
            updateCode:list[ThreeAddressCode] = []
            for it in self.update:
                updateCode += it.visit(context=context).code
            code += updateCode
            gotoInit = GotoCode(
                type=ThreeAddressCodeType.Goto,
                offset= initLen - len(code) - 1
            )
            code.append(gotoInit)
            ifFalseGoto.offset = len(code) - ifFalseGoto.offset - 1
            return NodeVisitorReturn(code)
        else:
            raise(Error('void error'))

class WhileStatementASTNode(BasicASTNode):
    def __init__(self, condition, body) -> None:
        super().__init__(WhileStatementType)
        self.condition:ValueASTNode = condition
        self.body:StatementASTNode = body
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        condRes = self.condition.visit(context=context)
        code += condRes.code
        if condRes.dst is not None:
            ifFalseGoto = IfGotoCode(
                type=ThreeAddressCodeType.IfGoto,
                src=condRes.dst,
                target= False,
                offset= len(code)
            )
            code.append(ifFalseGoto)
            bodyRes = self.body.visit(context=context)
            code += bodyRes.code
            code.append(GotoCode(type=ThreeAddressCodeType.Goto,offset=-len(code)-1))
        else:
            raise(Error('void error'))
        return NodeVisitorReturn(code)

class StatementListASTNode(BasicASTNode):
    def __init__(self, createContext = False) -> None:
        super().__init__(StatementListType)
        self.createContext = createContext
        self.statements:list[StatementASTNode] = []
        self.haveReturn = False
    
    def merge(self,other):
        if other.haveReturn:
            self.haveReturn = True
        if other.createContext:
            self.statements.append(other)
        else:
            for it in other.statements:
                self.statements.append(it)
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        if self.createContext:
            sTable = SymbolTable()
            sTable.father = context.symbols
            context = Context(symbols=sTable,globalFns=context.globalFns,fnName = context.fnName)
        code:list[ThreeAddressCode] = []
        for stat in self.statements:
            code += stat.visit(context).code
            if stat.type == FunctionReturnType:
                break
            elif stat.type == IfStatementType and stat.haveReturn():
                break
        return NodeVisitorReturn(code)

class IfStatementASTNode(BasicASTNode):
    def __init__(self, condition, body, elseBody=None) -> None:
        super().__init__(IfStatementType)
        self.condition:ValueASTNode = condition
        self.body:StatementASTNode = body
        self.elseBody: StatementASTNode = elseBody
    
    def haveReturn(self):
        if self.elseBody is not None:
            if (self.body.type == FunctionReturnType and
                self.body.src is not None) or (
                self.body.type == StatementListType and
                self.body.haveReturn
            ):
                if (self.elseBody.type == FunctionReturnType and 
                    self.body.src is not None) or (
                    self.elseBody.type == StatementListType and 
                    self.elseBody.haveReturn
                ):
                    return True
        return False

    def visit(self, context: Context) -> NodeVisitorReturn:
        code:list[ThreeAddressCode] = []
        condRes = self.condition.visit(context)
        code += condRes.code
        if condRes.dst is not None:
            ifFalseGoto = IfGotoCode(
                type=ThreeAddressCodeType.IfGoto,
                src=condRes.dst,
                target=False,
                offset=len(code)
            )
            code.append(ifFalseGoto)
            bodyRes = self.body.visit(context)
            code += bodyRes.code
            if self.elseBody is not None:
                trueGoto = GotoCode(
                    type = ThreeAddressCodeType.Goto,
                    offset=len(code)
                )
                code.append(trueGoto)
                ifFalseGoto.offset = len(code) - trueGoto.offset -1
                elseRes = self.elseBody.visit(context=context)
                code += elseRes.code
                trueGoto.offset = len(code) - trueGoto.offset -1
            else:
                ifFalseGoto.offset = len(code) - ifFalseGoto.offset - 1
        else:
            raise(Error('void error'))
        return NodeVisitorReturn(code)

StatementASTNode = Union[StatementListASTNode,ValueASTNode,DefineListASTNode,FunctionReturnASTNode,IfStatementASTNode,WhileStatementASTNode,ForStatementASTNode]


class FunctionASTNode(BasicASTNode):
    def __init__(self, name,args,returnType,statements: StatementListASTNode) -> None:
        super().__init__(FunctionDef)
        self.name = name
        self.args: ArgDefineListASTNode = args
        self.returnType = returnType
        self.statements:list[StatementASTNode] = []
        for it in statements.statements:
            self.statements.append(it)
        self.haveReturn = statements.haveReturn
    def getArgsType(self):
        return self.args.defs
    
    def visit(self, context: Context) -> NodeVisitorReturn:
        if self.returnType == voidType:
            if self.haveReturn:
                raise(Error(f'function "{self.name}" should return void'))
            else:
                if not self.haveReturn:
                    raise(Error(f'function "{self.name}" does not have Return statement'))
        sTable = SymbolTable()
        sTable.father = context.symbols
        context = Context(symbols=sTable,globalFns=context.globalFns,fnName=context.fnName)
        self.args.visit(context)

        code:list[ThreeAddressCode] = []
        for stat in self.statements:
            code == stat.visit(context=context).code
            if stat.type == FunctionReturnType:
                break
            elif stat.type == IfStatementType and stat.haveReturn():
                break
        
        if not self.haveReturn:
            code.append(FunctionReturnCode(
                type=ThreeAddressCodeType.FunctionReturn,
                name=self.name
            ))
        return NodeVisitorReturn(code)

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
