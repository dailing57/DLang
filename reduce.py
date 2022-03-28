from .ast import *
def functionOverall(fn,value,L,argList:ArgDefineListASTNode,R,type,LB,body:StatementListASTNode,RB,rest:RootASTNode):
    body.createContext = True
    fnNode = FunctionASTNode(value,argList,type,body)
    root = RootASTNode()
    root.fns.append(fnNode)
    root.merge(rest)
    return root

def mainOverall(fn,main,L,argList:ArgDefineListASTNode,R,LB,body:StatementListASTNode,RB):
    root = RootASTNode()
    body.createContext = True
    root.main = FunctionASTNode(Main,argList,voidType,body)
    return root

def returnType(arrow,type):
    return type

def returnVoid():
    return voidType

def argDefineList(arg,comma,other):
    aList = ArgDefineListASTNode()
    aList.defs.append(arg)
    aList.merge(other=other)
    return aList

def argDefine(arg):
    aList = ArgDefineListASTNode()
    aList.defs.append(arg)
    return aList

def nullArgDefine():
    return ArgDefineListASTNode()

tmpCnt = 0
def clear():
    global tmpCnt
    tmpCnt = 0

def genVariable(type=None,name=None):
    global tmpCnt
    if name is not None:
        return Variable(
            id= -1,
            name=name,
            type=type,
            isArg=False,
            isConst=False,
            isGlobal=False
        )
    else:
        tmpCnt += 1
        tot = tmpCnt
        return Variable(
            id= tot,
            name='$' + str(tot),
            type=type,
            isArg=False,
            isConst=True,
            isGlobal=False
        )

def argDefineType(value,colon,type):
    arg = genVariable(type,value)
    arg.isArg = True
    return arg

def statementList(statement:StatementASTNode,list:StatementListASTNode):
    sts = StatementListASTNode()
    if statement.type == FunctionReturnType and statement.src is not None:
        sts.haveReturn = True
    elif statement.type == IfStatementType:
        if statement.haveReturn():
            sts.haveReturn = True
    sts.statements.append(statement)
    sts.merge(list)
    return sts

def statementOpen(statement: IfStatementASTNode, list: StatementListASTNode):
    sts = StatementListASTNode()
    if statement.haveReturn():
        sts.haveReturn = True
    sts.statements.append(statement)
    sts.merge(list)
    return sts

def statementEmpty():
    return StatementListASTNode()

def statement(lt,dList:DefineListASTNode,Semicolon):
    return dList

def statementConst(ct,dList:DefineListASTNode,Semi):
    dList.isConst = True
    for it in dList.defs:
        it.dst.isConst = True
    return dList