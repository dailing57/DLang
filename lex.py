from DLex.ReParser import IToken
KeyWord = {
    'fn',
    'return',
    'main',
    'let',
    'const',
    'if',
    'else',
    'for',
    'while',
    'numberType',
    'floatType',
    'stringType',
    'boolType',
    'True',
    'False'
}

LexConfig = {
    'Identifier': IToken(
        rule='[_a-zA-Z][_a-zA-Z0-9]*',
    ),
    'Number': IToken(
        rule='[0-9]+.?',
        valCal=lambda x: int(x)
    ),
    'Float': IToken(
        rule='([0-9]+.[0-9]+|.[0-9]+)',
        valCal=lambda x: float(x)
    ),
    'String': IToken(
        rule='"([ !#-\\[\\[-~]|\\\\\\\\|\\\\")*"',
        valCal=lambda x: x[1:-1]
    ),
    'Plus': IToken(rule='\\+'),
    'Minus': IToken(rule='-'),
    'Mul': IToken(rule='\\*'),
    'Div': IToken(rule='/'),
    'Mod': IToken(rule='%'),
    'Assign': IToken(rule='='),
    'Comma': IToken(rule=','),
    'Colon': IToken(rule=':'),
    'DoubleColon': IToken(rule='::'),
    'Semicolon': IToken(rule=';'),
    'Dot': IToken(rule='.'),
    'Not': IToken(rule='!'),
    'And': IToken(rule='&&'),
    'Or': IToken(rule='\\|\\|'),
    'Equal': IToken(rule='=='),
    'NotEqual': IToken(rule='!='),
    'LessThan': IToken(rule='<'),
    'MoreThan': IToken(rule='>'),
    'LessOrEqual': IToken(rule='<='),
    'MoreOrEqual': IToken(rule='>='),
    'LRound': IToken(rule='\\('),
    'RRound': IToken(rule='\\)'),
    'LBrace': IToken(rule='{'),
    'RBrace': IToken(rule='}'),
    'ToArrow': IToken(rule='->'),
    'Comment': IToken(
        rule='//[ -~]*',
        valCal=lambda x: x[2:]
    ),
}
