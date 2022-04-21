# from dlang import DLang

# inputCode = open('./test/array-zh.dl', 'r', encoding='utf-8')
# dl = DLang()
# tmp = dl.compile(inputCode)
# # print(tmp.msg)
# dl.run(tmp)

def genFun(d):
    def oriFun(a):
        return a+d
    return oriFun


f = genFun(10)
print(f(1))
