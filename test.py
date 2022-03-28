from DLex import *
from DLex import ReParser
from lex import LexConfig, KeyWord

lp = ReParser.LexParser(LexConfig,True,keword=KeyWord)
code = open('./test/codeRe', 'r')
tokens = lp.parse(code)
for it in tokens:
    print(it)
