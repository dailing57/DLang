from index import DLang

inputCode = open('./test/gpa.dl', 'r')
dl = DLang()
tmp = dl.compile(inputCode)
# print(tmp.msg)
dl.run(tmp)
