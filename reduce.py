from AST import *


def functionOverall(fn, value, L, argList: ArgDefineListASTNode, R, type, LB, body: StatementListASTNode, RB, rest: RootASTNode):
    value = value.value
    body.createContext = True
    fnNode = FunctionASTNode(value, argList, type, body)
    root = RootASTNode()
    root.fns.append(fnNode)
    root.merge(rest)
    return root


def mainOverall(fn, main, L, argList: ArgDefineListASTNode, R, LB, body: StatementListASTNode, RB):
    root = RootASTNode()
    body.createContext = True
    root.main = FunctionASTNode(Main, argList, voidType, body)
    return root


def returnType(arrow, type):
    return type


def returnVoid():
    return voidType


def argDefineList(arg, comma, other):
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


def genVariable(type=None, name=None):
    global tmpCnt
    if name is not None:
        return Variable(
            id=-1,
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
            id=tot,
            name='$' + str(tot),
            type=type,
            isArg=False,
            isConst=True,
            isGlobal=False
        )


def argDefineType(value, colon, type):
    value = value.value
    arg = genVariable(type, value)
    arg.isArg = True
    return arg


def statementList(statement: StatementASTNode, list: StatementListASTNode):
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


def statement(lt, dList: DefineListASTNode, Semicolon):
    return dList


def statementConst(ct, dList: DefineListASTNode, Semi):
    dList.isConst = True
    for it in dList.defs:
        it.dst.isConst = True
    return dList


def statementAssign(value, assign, expr, semi):
    value = value.value
    return UnitOPASTNode(
        type=Assign,
        dst=genVariable(None, value),
        src=expr
    )


def statementBrace(l, list: StatementListASTNode, r):
    list.createContext = True
    return list


def statementExpr(node: ValueASTNode, semi):
    return node


def statementFunctionReturn(node: FunctionReturnASTNode, semi):
    return node


def statementIfElse(f, l, expr: ValueASTNode, r, body: StatementASTNode, el, elseBody: StatementASTNode):
    return IfStatementASTNode(expr, body, elseBody=elseBody)


def statementWhile(whl, l, expr: ValueASTNode, r, body: StatementASTNode):
    return WhileStatementASTNode(expr, body)


def statementFor(f, L, init, s1, condExpr: ValueASTNode, s2, assignList: list[UnitOPASTNode], R, body: StatementASTNode):
    return ForStatementASTNode(init, condExpr, assignList, body)


def ForInitLet(lt, list: DefineListASTNode):
    return list


def ForInitAssignList(list: list[UnitOPASTNode]):
    return list


def ForAssignEmpty():
    return []


def ForAssignList(value, ag, expr: ValueASTNode, other: list[UnitOPASTNode]):
    value = value.value
    return [UnitOPASTNode(Assign, genVariable(None, value), expr), *other]


def ForIdAssign(value, ag, expr: ValueASTNode):
    value = value.value
    return UnitOPASTNode(Assign, genVariable(None, value), expr)


def openStatementS(f, l, expr: ValueASTNode, r, body: StatementASTNode):
    return IfStatementASTNode(expr, body=body)


def openStatementIfEl(f, l, expr: ValueASTNode, r, body: StatementASTNode, el, elseBody: StatementASTNode):
    return IfStatementASTNode(expr, body=body, elseBody=elseBody)


def functionReturnEmpty():
    return FunctionReturnASTNode()


def functionExpr(ret, expr: ValueASTNode):
    rNode = FunctionReturnASTNode()
    rNode.src = expr
    return rNode


def returnType(arr, type):
    return type


def defineId(value):
    value = value.value
    return DefineASTNode(genVariable(None, value))


def defineIdType(value, colon, type):
    value = value.value
    return DefineASTNode(genVariable(type, value))


def defineAssign(value, colon, expr: ValueASTNode):
    value = value.value
    return DefineASTNode(genVariable(expr.dst.type, value), expr)


def defineAssignT(value, colon, type, expr):
    value = value.value
    return DefineASTNode(genVariable(type, value), expr)


def defineList(d: DefineASTNode, comma, other: DefineListASTNode):
    dlist = DefineListASTNode()
    dlist.defs.append(d)
    dlist.merge(other)
    return dlist


def defineListE(d: DefineASTNode):
    dlist = DefineListASTNode()
    dlist.defs.append(d)
    return dlist


def genLiteral(type, value):
    return Literal(type, value)


def plus(term: ValueASTNode, p, expr: ValueASTNode):
    type = getBinOPType(Plus, term.dst.type, expr.dst.type)
    return BinOPASTNode(Plus, genVariable(type), term, expr)


def minus(term: ValueASTNode, m, expr: ValueASTNode):
    type = getBinOPType(Minus, term.dst.type, expr.dst.type)
    return BinOPASTNode(Minus, genVariable(type), term, expr)


def ExprTerm(node):
    return node


def termMul(factor: ValueASTNode, mul, term: ValueASTNode):
    type = getBinOPType(Mul, factor.dst.type, term.dst.type)
    return BinOPASTNode(Mul, genVariable(type), type, term)


def termDiv(factor: ValueASTNode, div, term: ValueASTNode):
    type = getBinOPType(Div, factor.dst.type, term.dst.type)
    return BinOPASTNode(Div, genVariable(type), type, term)


def termMod(factor: ValueASTNode, mod, term: ValueASTNode):
    type = getBinOPType(Mod, factor.dst.type, term.dst.type)
    return BinOPASTNode(Mod, genVariable(type), type, term)


def factorPlus(p, node):
    return node


def factorminus(m, node: ValueASTNode):
    return UnitOPASTNode(Negative, genVariable(node.dst.type), node)


def factornot(m, node: ValueASTNode):
    return UnitOPASTNode(Not, genVariable(node.dst.type), node)


def rightVal(node):
    return node


def roundexpr(l, node, r):
    return node


def exprminus(m, l, node: ValueASTNode, r):
    return UnitOPASTNode(Negative, genVariable(node.dst.type), node)


def exprnot(n, l, node: ValueASTNode, r):
    return UnitOPASTNode(Not, genVariable(node.dst.type), node)


def functionCall(value, l, args: FunctionCallArgListASTNode, r):
    fnCall = FunctionCallASTNode(value.value, args)
    return fnCall


def functionCallNamespace(namespace, dc, value, l, args: FunctionCallArgListASTNode, r):
    fnCall = FunctionCallASTNode(namespace.value+'::'+value.value, args=args)
    return fnCall


def callArgList(expr: ValueASTNode, comma, rest: FunctionCallArgListASTNode):
    fnalist = FunctionCallArgListASTNode()
    fnalist.args.append(expr)
    fnalist.merge(rest)
    return fnalist


def callArgListEnd(expr: ValueASTNode):
    fnalist = FunctionCallArgListASTNode()
    fnalist.args.append(expr)
    return fnalist
