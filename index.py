from DLex.ReParser import *
from DParse.LRParser import *
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


class IHooks:
    def __init__(self, beforeRunHooks=None, afterRunHooks=None) -> None:
        self.beforeRun = beforeRunHooks
        self.afterRun = afterRunHooks


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
        self.hooks = IHooks(beforeRunHooks=beforeRunHooks,
                            afterRunHooks=afterRunHooks)

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

    def argParse(self, val):
        if not isnan(int(val)):
            return LiteralCode(int(val), numberType)
        elif not isnan(float(val)):
            return LiteralCode(float(val), floatType)
        elif not val == true:
            return LiteralCode(true, boolType)
        elif not val == false:
            return LiteralCode(false, boolType)
        else:
            return LiteralCode(val, stringType)

    def run(self, cp: CompileOut, args: list[str] = [], inp: list[str] = []):
        for fn in self.hooks.beforeRun:
            fn(inp)
        code = cp.code
        globalFns = cp.globalFns
        arg = list(map(self.argParse, args))
        mainArg = cp.root.main.getArgsType() if cp.root.main is not None else []
        if len(mainArg) > len(arg):
            raise(Error(
                f'function "main" needs {len(mainArg)} args, but you only provide {len(arg)} args'))
        arg = arg[:len(mainArg)]
        for i in range(len(arg)):
            if mainArg[i] == stringType:
                arg[i].value = str(arg[i].value)
                arg[i].type = stringType
            else:
                if arg[i].type == stringType:
                    raise(Error('function "main" arg list is not matched'))
                if mainArg[i] == numberType:
                    if arg[i].type == floatType:
                        arg[i].value = round(arg[i].value)
                        arg[i].value = numberType
                    elif arg[i].type == boolType:
                        arg[i].value = int(arg[i].value)
                        arg[i].type = numberType
                elif arg[i].value == floatType:
                    arg[i].value = int(arg[i].value)
                    arg[i].value = floatType
                elif mainArg[i] == boolType:
                    arg[i].value = True if arg[i].value != 0 else False
                    arg[i].type = boolType
        vm(code, globalFns, arg)
