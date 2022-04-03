from DLex.ReParser import IToken
# keyWord
Fn = 'fn'
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
true = 'True'
false = 'False'

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
        rule='[_a-zA-Z][_a-zA-Z0-9]*',
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
