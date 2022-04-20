from DLex.ReParser import *
from lex_zh import LexConfig, KeyWord
DLangLexer = LexParser(LexConfig, True, KeyWord)
inputCode = open('./test/han.dl', 'r', encoding='utf-8')
tokens = DLangLexer.parse(inputCode)
print(tokens)
