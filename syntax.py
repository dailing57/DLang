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
                    ARGDEFINEList,
                    RRound,
                    RETURNTYPE,
                    LBrace,
                    STATEMENTList,
                    RBrace,
                    PROGRAM
                ],
                reduce = functionOverall
            ),
            ProductionRightRule(
                rule=[
                    Fn,
                    Main,
                    LRound,
                    ARGDEFINEList,
                    RRound,
                    LBrace,
                    STATEMENTList,
                    RBrace
                ],
                reduce= mainOverall
            )
        ]
    ),
    ProductionRule(
        left=RETURNTYPE,
        right=[
            ProductionRightRule(
                rule=[ToArrow,TYPES],
                reduce=returnType
            ),
            ProductionRightRule(
                rule=[],
                reduce=returnVoid
            )
        ]
    ),
    ProductionRule(
        left=ARGDEFINEList,
        right=[
            ProductionRightRule(
                rule=[ARGDEFINE,Comma,ARGDEFINEList],
                reduce=argDefineList
            ),
            ProductionRightRule(
                rule=[ARGDEFINE],
                reduce=argDefine
            ),
            ProductionRightRule(
                rule=[],
                reduce=nullArgDefine
            )
        ]
    ),
    ProductionRule(
        left=ARGDEFINE,
        right=[
            ProductionRightRule(
                rule=[Identifier,Colon,TYPES],
                reduce=argDefineType
            )
        ]
    ),
    ProductionRule(
        left=STATEMENTList,
        right=[
            ProductionRightRule(
                rule=[STATEMENT,STATEMENTList],
                reduce=statementList
            ),
            ProductionRightRule(
                rule=[OPENSTATEMENT,STATEMENTList],
                reduce=statementOpen
            ),
            ProductionRightRule(
                rule=[],
                reduce=statementEmpty
            )
        ]
    ),
    ProductionRule(
        left=STATEMENT,
        right=[
            ProductionRightRule(
                rule=[Let,DEFINEList,Semicolon],
                reduce=statement
            ),
            ProductionRightRule(
                rule = [Const,DEFINEList,Semicolon],
                reduce=statementConst
            )
        ]
    )
]
