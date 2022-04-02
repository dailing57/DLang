from index import DLang

inputCode = open('./test/helloWorld.dl', 'r')
dl = DLang()
tmp = dl.compile(inputCode)
dl.run(tmp)
