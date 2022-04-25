import dill
from dlang import *


def main():
    dl = DLang('en')
    with open('./seri/DLangLexer-en', 'wb') as f:
        dill.dump(dl.DLangLexer, f)
    with open('./seri/DLangParser-en', 'wb') as f:
        dill.dump(dl.DLangParser, f)


if __name__ == '__main__':
    main()
