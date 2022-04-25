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
                reduce=functionOverall
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
                reduce=mainOverall
            )
        ]
    ),
    ProductionRule(
        left=RETURNTYPE,
        right=[
            ProductionRightRule(
                rule=[ToArrow, TYPES],
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
                rule=[ARGDEFINE, Comma, ARGDEFINEList],
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
                rule=[Identifier, Colon, TYPES],
                reduce=argDefineType
            )
        ]
    ),
    ProductionRule(
        left=STATEMENTList,
        right=[
            ProductionRightRule(
                rule=[STATEMENT, STATEMENTList],
                reduce=statementList
            ),
            ProductionRightRule(
                rule=[OPENSTATEMENT, STATEMENTList],
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
                rule=[Let, DEFINEList, Semicolon],
                reduce=statement
            ),
            ProductionRightRule(
                rule=[Const, DEFINEList, Semicolon],
                reduce=statementConst
            ),
            ProductionRightRule(
                rule=[Identifier, Assign, EXPR, Semicolon],
                reduce=statementAssign
            ),
            ProductionRightRule(
                rule=[LBrace, STATEMENTList, RBrace],
                reduce=statementBrace
            ),
            ProductionRightRule(
                rule=[EXPR, Semicolon],
                reduce=statementExpr
            ),
            ProductionRightRule(
                rule=[FUNCTIONRETURN, Semicolon],
                reduce=statementFunctionReturn
            ),
            ProductionRightRule(
                rule=[
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
                rule=[While, LRound, LOGICALEXPR, RRound, STATEMENT],
                reduce=statementWhile
            ),
            ProductionRightRule(
                rule=[
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
                rule=[Let, DEFINEList],
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
                rule=[Identifier, Assign, EXPR, Comma, FORASSIGNList],
                reduce=ForAssignList
            ),
            ProductionRightRule(
                rule=[Identifier, Assign, EXPR],
                reduce=ForIdAssign
            )
        ]
    ),
    ProductionRule(
        left=OPENSTATEMENT,
        right=[
            ProductionRightRule(
                rule=[If, LRound, LOGICALEXPR, RRound, STATEMENT],
                reduce=openStatementS
            ),
            ProductionRightRule(
                rule=[If, LRound, LOGICALEXPR, RRound, OPENSTATEMENT],
                reduce=openStatementS
            ),
            ProductionRightRule(
                rule=[If, LRound, LOGICALEXPR, RRound,
                      STATEMENT, Else, OPENSTATEMENT],
                reduce=openStatementIfEl
            )
        ]
    ),
    ProductionRule(
        left=FUNCTIONRETURN,
        right=[
            ProductionRightRule(
                rule=[Return],
                reduce=functionReturnEmpty
            ),
            ProductionRightRule(
                rule=[Return, EXPR],
                reduce=functionExpr
            ),
            ProductionRightRule(
                rule=[Return, LOGICALEXPR],
                reduce=functionExpr
            )
        ]
    ),
    ProductionRule(
        left=TYPES,
        right=[
            ProductionRightRule(
                rule=[numberType],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[complexType],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[floatType],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[stringType],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[boolType],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[functionType],
                reduce=(lambda tk:tk.type)
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
                rule=[Identifier, Colon, TYPES],
                reduce=defineIdType
            ),
            ProductionRightRule(
                rule=[Identifier, Assign, EXPR],
                reduce=defineAssign
            ),
            ProductionRightRule(
                rule=[Identifier, Colon, TYPES, Assign, EXPR],
                reduce=defineAssignT
            ),
            ProductionRightRule(
                rule=[Identifier,
                      Colon,
                      TYPES,
                      Assign,
                      LRound,
                      ARGDEFINEList,
                      RRound,
                      RETURNTYPE,
                      LBrace,
                      STATEMENTList,
                      RBrace],
                reduce=defineLocalFunction
            ),
        ]
    ),
    ProductionRule(
        left=DEFINEList,
        right=[
            ProductionRightRule(
                rule=[DEFINE, Comma, DEFINEList],
                reduce=defineList
            ),
            ProductionRightRule(
                rule=[DEFINE],
                reduce=defineListE
            )
        ]
    )
]

ExprProduction = [
    ProductionRule(
        left=EXPR,
        right=[
            ProductionRightRule(
                rule=[Term, Plus, EXPR],
                reduce=plus
            ),
            ProductionRightRule(
                rule=[Term, Minus, EXPR],
                reduce=minus
            ),
            ProductionRightRule(
                rule=[Term],
                reduce=ExprTerm
            )
        ]
    ),
    ProductionRule(
        left=Term,
        right=[
            ProductionRightRule(
                rule=[Factor, Mul, Term],
                reduce=termMul
            ),
            ProductionRightRule(
                rule=[Factor, Div, Term],
                reduce=termDiv
            ),
            ProductionRightRule(
                rule=[Factor, Mod, Term],
                reduce=termMod
            ),
            ProductionRightRule(
                rule=[Factor],
                reduce=ExprTerm
            )
        ]
    ),
    Production(
        left=Factor,
        right=[
            ProductionRightRule(
                rule=[Plus, RightValue],
                reduce=factorPlus
            ),
            ProductionRightRule(
                rule=[Minus, RightValue],
                reduce=factorminus
            ),
            ProductionRightRule(
                rule=[Not, RightValue],
                reduce=factornot
            ),
            ProductionRightRule(
                rule=[RightValue],
                reduce=rightVal
            ),
            ProductionRightRule(
                rule=[LRound, EXPR, RRound],
                reduce=roundexpr
            ),
            ProductionRightRule(
                rule=[Plus, LRound, EXPR, RRound],
                reduce=(lambda p, l, node, r:node)
            ),
            ProductionRightRule(
                rule=[Minus, LRound, EXPR, RRound],
                reduce=exprminus
            ),
            ProductionRightRule(
                rule=[Not, LRound, EXPR, RRound],
                reduce=exprnot
            )
        ]
    ),
    ProductionRule(
        left=RightValue,
        right=[
            ProductionRightRule(
                rule=[Number],
                reduce=(lambda tk:LeafASTNode(
                        genLiteral(numberType, tk.value)))
            ),
            ProductionRightRule(
                rule=[ComplexD],
                reduce=(lambda tk:LeafASTNode(
                        genLiteral(complexType, tk.value)))
            ),
            ProductionRightRule(
                rule=[true],
                reduce=(lambda tk:LeafASTNode(genLiteral(boolType, True)))
            ),
            ProductionRightRule(
                rule=[false],
                reduce=(lambda tk:LeafASTNode(genLiteral(boolType, False)))
            ),
            ProductionRightRule(
                rule=[Float],
                reduce=(lambda tk:LeafASTNode(
                        genLiteral(floatType, tk.value)))
            ),
            ProductionRightRule(
                rule=[String],
                reduce=(lambda tk:LeafASTNode(
                        genLiteral(stringType, tk.value)))
            ),
            ProductionRightRule(
                rule=[Identifier],
                reduce=(lambda tk:LeafASTNode(genVariable(None, tk.value)))
            ),
            ProductionRightRule(
                rule=[FUNCTIONCALL],
                reduce=(lambda call:call)
            )
        ]
    ),
    ProductionRule(
        left=FUNCTIONCALL,
        right=[
            ProductionRightRule(
                rule=[Identifier, LRound, CALLARGList, RRound],
                reduce=functionCall
            ),
            ProductionRightRule(
                rule=[
                    Identifier,
                    DoubleColon,
                    Identifier,
                    LRound,
                    CALLARGList,
                    RRound
                ],
                reduce=functionCallNamespace
            )
        ]
    ),
    ProductionRule(
        left=CALLARGList,
        right=[
            ProductionRightRule(
                rule=[EXPR, Comma, CALLARGList],
                reduce=callArgList
            ),
            ProductionRightRule(
                rule=[EXPR],
                reduce=callArgListEnd
            ),
            ProductionRightRule(
                rule=[],
                reduce=(lambda: FunctionCallArgListASTNode())
            )
        ]
    )
]

LogicalProduction = [
    ProductionRule(
        left=LOGICALEXPR,
        right=[
            ProductionRightRule(
                rule=[LOGICALAND],
                reduce=(lambda expr:expr)
            ),
            ProductionRightRule(
                rule=[LOGICALAND, Or, LOGICALEXPR],
                reduce=(lambda cmp, o, expr:BinOPASTNode(
                        Or, genVariable(boolType), cmp, expr))
            )
        ]
    ),
    ProductionRule(
        left=LOGICALAND,
        right=[
            ProductionRightRule(
                rule=[CMP],
                reduce=(lambda cmp:cmp),
            ),
            ProductionRightRule(
                rule=[CMP, And, LOGICALAND],
                reduce=(lambda cmp, ad, expr:BinOPASTNode(
                        And, genVariable(boolType), cmp, expr))
            )
        ],
    ),
    ProductionRule(
        left=CMP,
        right=[
            ProductionRightRule(
                rule=[EXPR, CMPToken, EXPR],
                reduce=(lambda lexpr, type, rexpr:BinOPASTNode(
                        type, genVariable(boolType), lexpr, rexpr)),
            ),
            ProductionRightRule(
                rule=[LRound, LOGICALEXPR, RRound],
                reduce=(lambda l, expr, r: expr)
            )
        ],
    ),
    ProductionRule(
        left=CMPToken,
        right=[
            ProductionRightRule(
                rule=[Equal],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[NotEqual],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[LessThan],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[MoreThan],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[LessOrEqual],
                reduce=(lambda tk:tk.type)
            ),
            ProductionRightRule(
                rule=[MoreOrEqual],
                reduce=(lambda tk:tk.type)
            )
        ]
    )
]

tks = []
for it in LexConfig:
    tks.append(it)


def beforeCreated(*args):
    clear()
    clearAST()


def created(root: RootASTNode, bindedFns: dict[str, BuiltinFunction]):
    context = Context(symbols=SymbolTable(), globalFns=bindedFns, fnName=Main)
    res = root.visit(context=context)
    return root, res.code, context.globalFns


config = ParserConfig(
    hooks=ParserHooks(
        beforeCreated=beforeCreated,
        created=created
    ),
    tokens=[*tks, *KeyWord],
    types=[
        PROGRAM,
        STATEMENTList,
        STATEMENT,
        OPENSTATEMENT,
        TYPES,
        ARGDEFINE,
        ARGDEFINEList,
        FORInit,
        FORASSIGNList,
        RETURNTYPE,
        DEFINE,
        DEFINEList,
        EXPR,
        Term,
        Factor,
        RightValue,
        FUNCTIONCALL,
        CALLARGList,
        FUNCTIONRETURN,
        LOGICALEXPR,
        LOGICALAND,
        CMP,
        CMPToken
    ],
    start=PROGRAM,
    productions=[*StatementProduction, *ExprProduction, *LogicalProduction]
)
