from DLex.ReParser import IToken
# keyWord
Fn = 'fun'
Return = 'return'
Main = 'main'
Let = 'let'
Const = 'const'
If = 'if'
Else = 'else'
For = 'for'
While = 'while'
numberType = 'number'
floatType = 'float'
stringType = 'string'
boolType = 'bool'
complexType = 'complex'
functionType = 'function'
true = 'True'
false = 'False'
# VoidType
voidType = 'void'
# CmpOPType
NotEqual = 'NotEqual'
Equal = 'Equal'
LessThan = 'LessThan'
MoreThan = 'MoreThan'
LessOrEqual = 'LessOrEqual'
MoreOrEqual = 'MoreOrEqual'

# BinOPType
Plus = 'Plus'
Minus = 'Minus'
Mul = 'Mul'
Div = 'Div'
Mod = 'Mod'
Negative = 'Negative'
Not = 'Not'
And = 'And'
Or = 'Or'

# UnitOPType
Negative = 'Negative'
Not = 'Not'
Assign = 'Assign'

# punctuation
Comma = 'Comma'
Colon = 'Colon'
DoubleColon = 'DoubleColon'
Semicolon = 'Semicolon'
Dot = 'Dot'
LRound = 'LRound'
RRound = 'RRound'
LBrace = 'LBrace'
RBrace = 'RBrace'
ToArrow = 'ToArrow'
Comment = 'Comment'

Identifier = 'Identifier'
Number = 'Number'
Float = 'Float'
String = 'String'
ComplexD = 'Complex'
KeyWord = {
    Fn,
    Return,
    Main,
    Let,
    Const,
    If,
    Else,
    For,
    While,
    numberType,
    floatType,
    stringType,
    boolType,
    complexType,
    functionType,
    true,
    false
}

LexConfig = {
    Identifier: IToken(
        rule='[_a-zA-Z][_a-zA-Z0-9]*',
    ),
    Number: IToken(
        rule='[0-9]+.?',
        valCal=lambda x: int(x)
    ),
    Float: IToken(
        rule='([0-9]+.[0-9]+|.[0-9]+|[0-9].[0-9]+[eE][0-9]+)',
        valCal=lambda x: float(x)
    ),
    ComplexD: IToken(
        rule='[0-9]\\+[0-9]+i',
        valCal=lambda x: complex(x[:-1]+'j')
    ),
    String: IToken(
        rule='"([ !#-\\[\\[-~]|\\\\\\\\|\\\\")*"',
        valCal=lambda x: x[1:-1]
    ),
    Plus: IToken(rule='\\+'),
    Minus: IToken(rule='-'),
    Mul: IToken(rule='\\*'),
    Div: IToken(rule='/'),
    Mod: IToken(rule='%'),
    Assign: IToken(rule='='),
    Comma: IToken(rule=','),
    Colon: IToken(rule=':'),
    DoubleColon: IToken(rule='::'),
    Semicolon: IToken(rule=';'),
    Dot: IToken(rule='.'),
    Not: IToken(rule='!'),
    And: IToken(rule='&&'),
    Or: IToken(rule='\\|\\|'),
    Equal: IToken(rule='=='),
    NotEqual: IToken(rule='!='),
    LessThan: IToken(rule='<'),
    MoreThan: IToken(rule='>'),
    LessOrEqual: IToken(rule='<='),
    MoreOrEqual: IToken(rule='>='),
    LRound: IToken(rule='\\('),
    RRound: IToken(rule='\\)'),
    LBrace: IToken(rule='{'),
    RBrace: IToken(rule='}'),
    ToArrow: IToken(rule='->'),
    Comment: IToken(
        rule='//[ -~]*',
        valCal=lambda x: x[2:]
    ),
}

Lib_In = 'In'
Lib_hasNext = 'hasNext'
Lib_nextNumber = 'nextNumber'
Lib_nextFloat = 'nextFloat'
Lib_nextString = 'nextString'
Lib_nextBool = 'nextBool'
Lib_Out = 'print'
Lib_Array = 'Array'
Lib_new = 'new'
Lib_assign = 'assign'
Lib_length = 'length'
Lib_push = 'push'
Lib_pop = 'pop'
Lib_get = 'get'
Lib_set = 'set'
Lib_clear = 'clear'
Lib_Delete = 'Delete'
Lib_String = 'String'
Lib_to_number = 'to_number'
Lib_to_float = 'to_float'
Lib_Number = Number
Lib_Complex = ComplexD
Lib_to_string = 'to_string'
Lib_max = 'max'
Lib_min = 'min'
Lib_abs = 'abs'
Lib_rand = 'rand'
Lib_Float = Float
Lib_floor = 'floor'
Lib_round = 'round'
Lib_ceil = 'ceil'
Lib_sqrt = 'sqrt'
