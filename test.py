# from index import DLang

# inputCode = open('./test/helloWorld.dl', 'r')
# dl = DLang()
# print(dl.compile(inputCode).ok)

def f(*args):
    print(*args)
    print(args)


f(1, 2, 3)
