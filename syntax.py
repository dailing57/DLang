from turtle import left
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
            ),
            ProductionRightRule(
                rule=[Identifier,Assign,EXPR,Semicolon],
                reduce=statementAssign
            ),
            ProductionRightRule(
                rule = [LBrace,STATEMENTList,RBrace],
                reduce=statementBrace
            ),
            ProductionRightRule(
                rule=[EXPR,Semicolon],
                reduce=statementExpr
            ),
            ProductionRightRule(
                rule=[FUNCTIONRETURN,Semicolon],
                reduce=statementFunctionReturn
            ),
            ProductionRightRule(
                rule = [
                    If,
                    LRound,
                    LOGICALEXPR,
                    RRound,
                    STATEMENT,
                    Else,
                    STATEMENT
                ],
                reduce=statementIfElse
            ),
            ProductionRightRule(
                rule = [While,LRound,LOGICALEXPR,RRound,STATEMENT],
                reduce=statementWhile
            ),
            ProductionRightRule(
                rule = [
                    For,
                    LRound,
                    FORInit,
                    Semicolon,
                    LOGICALEXPR,
                    Semicolon,
                    FORASSIGNList,
                    RRound,
                    STATEMENT
                ],
                reduce=statementFor
            )
        ]
    ),
    ProductionRule(
        left=FORInit,
        right=[
            ProductionRightRule(
                rule=[Let,DEFINEList],
                reduce=ForInitLet
            ),
            ProductionRightRule(
                rule=[FORASSIGNList],
                reduce=ForInitAssignList
            )
        ]
    ),
    ProductionRule(
        left=FORASSIGNList,
        right=[
            ProductionRightRule(
                rule=[],
                reduce=ForAssignEmpty
            ),
            ProductionRightRule(
                rule=[Identifier,Assign,EXPR,Comma,FORASSIGNList],
                reduce=ForAssignList
            ),
            ProductionRightRule(
                rule=[Identifier,Assign,EXPR],
                reduce=ForIdAssign
            )
        ]
    ),
    ProductionRule(
        left=OPENSTATEMENT,
        right=[
            ProductionRightRule(
                rule=[If,LRound,LOGICALEXPR,RRound,STATEMENT],
                reduce=openStatementS
            ),
            ProductionRightRule(
                rule=[If,LRound,LOGICALEXPR,RRound,OPENSTATEMENT],
                reduce=openStatementS
            ),
            ProductionRightRule(
                rule=[If,LRound,LOGICALEXPR,RRound,STATEMENT,Else,OPENSTATEMENT],
                reduce=openStatementIfEl
            )
        ]
    ),
    ProductionRule(
        left=FUNCTIONRETURN,
        right=[
            ProductionRightRule(
                left=[Return],
                reduce=functionReturnEmpty
            ),
            ProductionRightRule(
                left=[Return,EXPR],
                reduce=functionExpr
            ),
            ProductionRightRule(
                left=[Return,LOGICALEXPR],
                reduce=functionExpr
            )
        ]
    ),
    ProductionRule(
        left=TYPES,
        right=[
            ProductionRightRule(
                rule=[numberType],
                reduce=returnType
            ),
            ProductionRightRule(
                rule=[floatType],
                reduce=returnType
            ),
            ProductionRightRule(
                rule=[stringType],
                reduce=returnType
            ),
            ProductionRightRule(
                rule=[boolType],
                reduce=returnType
            ),
        ]
    ),
    ProductionRule(
        left=DEFINE,
        right=[
            ProductionRightRule(
                rule=[Identifier],
                reduce=defineId
            ),
            ProductionRightRule(
                rule=[Identifier,Colon,TYPES],
                reduce=defineIdType
            ),
            ProductionRightRule(
                rule=[Identifier,Assign,EXPR],
                reduce=defineAssign
            ),
            ProductionRightRule(
                rule=[Identifier,Colon,TYPES,Assign,EXPR],
                reduce=defineAssignT
            ),
        ]
    )
]
