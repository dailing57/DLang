from index import DLang

inputCode = open('./test/han.dl', 'r', encoding='utf-8')
dl = DLang()
tmp = dl.compile(inputCode)
# print(tmp.msg)
dl.run(tmp)
