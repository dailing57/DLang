from index import DLang

inputCode = open('./test/helloWorld.dl', 'r')
dl = DLang()
tmp = dl.compile(inputCode)
print(tmp.ok, tmp.msg, tmp.tk)
