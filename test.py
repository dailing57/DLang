from index import DLang

inputCode = open('./test/helloWorld.dl','r')
DLang.run(DLang.compile(inputCode))
