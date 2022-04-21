from DLex.ReParser import IToken
# keyWord
Fn = '函'
Return = '得'
Main = '主'
Let = '令'
Const = '静'
If = '若'
Else = '否则'
For = '遍'
While = '当'
numberType = '整'
floatType = '浮'
stringType = '串'
boolType = '判'
true = '真'
false = '假'
# VoidType
voidType = '空'
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
Number = '整型'
Float = '浮型'
String = '串型'

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
    true,
    false
}

LexConfig = {
    Identifier: IToken(
        rule='[_a-zA-Z一-龥][_a-zA-Z0-9一-龥]*',
    ),
    Number: IToken(
        rule='[0-9]+.?',
        valCal=lambda x: int(x)
    ),
    Float: IToken(
        rule='([0-9]+.[0-9]+|.[0-9]+)',
        valCal=lambda x: float(x)
    ),
    String: IToken(
        rule='"([一-龥 !#-\\[\\[-~]|\\\\\\\\|\\\\")*"',
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
        rule='//[ -~一-龥]*',
        valCal=lambda x: x[2:]
    ),
}

Lib_In = '入'
Lib_hasNext = '有下一个？'
Lib_nextNumber = '下一个整'
Lib_nextFloat = '下一个浮'
Lib_nextString = '下一个串'
Lib_nextBool = '下一个判'
Lib_Out = '出'
Lib_Array = '组'
Lib_new = '创'
Lib_assign = '赋'
Lib_length = '长'
Lib_push = '压'
Lib_pop = '弹'
Lib_get = '拿'
Lib_set = '置'
Lib_clear = '清'
Lib_Delete = '删'
Lib_String = '串型'
Lib_to_number = '变整'
Lib_to_float = '变浮'
Lib_Number = '整型'
Lib_to_string = '变串'
Lib_max = '最大'
Lib_min = '最小'
Lib_abs = '绝对'
Lib_rand = '随机'
Lib_Float = '浮型'
Lib_floor = '下整'
Lib_round = '四舍'
Lib_ceil = '上整'
Lib_sqrt = '开方'
