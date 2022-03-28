from lex import *
from type import *
from ast import *
from symbolTable import *
from tac import *
from DParse.type import *
from reduce import *
PROGRAM = 'Program'
STATEMENTList = 'StatmentList'
STATEMENT = 'Statement'
OPENSTATEMENT = 'OpenStatement'
TYPES = 'Types'
ARGDEFINE = 'ArgDefine'
ARGDEFINEList = 'ArgDefineList'
FORInit = 'ForInit'
FORASSIGNList = 'ForAssignList'
RETURNTYPE = 'FunctionReturnType'
FUNCTIONCALL = 'FunctionCall'
CALLARGList = 'FunctionCallArgList'
FUNCTIONRETURN = 'FunctionReturn'
DEFINE = 'Define'
DEFINEList = 'DefineList'

EXPR = 'Expr'
Term = 'Term'
Factor = 'Factor'
RightValue = 'RightValue'

LOGICALEXPR = 'LogicalExpr'
LOGICALAND = 'LogicalAnd'
CMP = 'LogicalCmp'
CMPToken = 'CmpToken'

StatementProduction = [
    ProductionRule(
        left=PROGRAM,
        right=[
            ProductionRightRule(
                rule=[
                    Fn,
                    Identifier,
                    LRound,
                    RRound,
                    RETURNTYPE,
                    LBrace,
                    STATEMENTList,
                    RBrace,
                    PROGRAM
                ],
                reduce = functionOverall
            )
        ]
    )
]
