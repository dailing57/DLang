from dlang import DLang
from type import BuiltinFunction

inputCode = open('./test/fib-zh.dl', 'r', encoding='utf-8')
dl = DLang('zh')
tmp = dl.compile(inputCode)
for it in tmp.code:
    print(it)
for it in tmp.globalFns:
    if type(tmp.globalFns[it]) is not BuiltinFunction:
        print(tmp.globalFns[it])
