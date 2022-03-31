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
    def __init__(self, ok=False, msg=None) -> None:
        self.ok = ok
        self.msg = msg


def cleanAST():
    clear()
    clearAST()


def genAST(root: RootASTNode, bindedFns: dict[str, BuiltinFunction]):
    context = Context(symbols=SymbolTable(), globalFns=bindedFns, fnName=Main)
    res = root.visit(context=context)
    return CompileOut(code=res.code, globalFns=context.globalFns, root=root)


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
            ok, val = DLangParser.parse(tokens)
            cp = genAST(val, bindedFns=self.bindedFns)
            if ok:
                cp.ok = True
                cp.tokens = tokens
                return cp
        except Error as e:
            return CompileErrorOut(ok=False, msg=e.message)

    def run(cp: CompileOut):
        vm(cp.code, cp.globalFns, [])
