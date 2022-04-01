from DLex.ReParser import *
from DParse.LRParser import *
from lex import LexConfig
from reduce import clear
from syntax import config as SyntaxConfig
from tac import *
from type import *
from vm import vm
from AST import *
from lib import *
from tac import *

DLangLexer = LexParser(LexConfig, True, KeyWord)
DLangParser = LRParser(SyntaxConfig)


class CompileOut:
    def __init__(self, tokens=[], root=None, code=None, globalFns=None, ok=True,) -> None:
        self.ok = ok
        self.tokens: list[Token] = tokens
        self.root: RootASTNode = root
        self.code: list[ThreeAddressCode] = code
        self.globalFns: dict[str, GlobalFunction] = globalFns


class CompileErrorOut:
    def __init__(self, ok=False, tk=None, msg=None) -> None:
        self.ok = ok
        self.tk = tk
        self.msg = msg


class DLang:
    def __init__(self) -> None:
        self.bindedFns: dict[str, BuiltinFunction] = {}
        for it in IOLib:
            self.bindedFns[it.name] = it
        for it in ArrayLib:
            self.bindedFns[it.name] = it
        for it in StringLib:
            self.bindedFns[it.name] = it
        for it in NumberLib:
            self.bindedFns[it.name] = it
        for it in FloatLib:
            self.bindedFns[it.name] = it

    def addFn(self, name, type, args, fn):
        self.bindedFns[name] = BuiltinFunction(type=type, args=args, fn=fn)

    def compile(self, text):
        try:
            tokens = DLangLexer.parse(text)
            ok, val = DLangParser.parse(tokens, self.bindedFns)
            if ok:
                return CompileOut(ok=True, tokens=tokens, root=val[0], code=val[1], globalFns=val[2])
            else:
                return CompileErrorOut(ok=False, tk=val)
        except Error as e:
            return CompileErrorOut(ok=False, msg=e.message)

    def run(self, cp: CompileOut, args: list[str] = [], input: list[str] = []):
        self.hoo
