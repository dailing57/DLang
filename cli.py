import argparse
from dlang import DLang


def main():
    parser = argparse.ArgumentParser(
        description='DLang - DL\'s Lang'
    )
    parser.add_argument('codefile', help='dlang code file')
    parser.add_argument('-a', '--nargs', nargs='+')
    parser.add_argument('-i', '--input')
    args = parser.parse_args()
    codefile = open(args.codefile, 'r', encoding='utf-8')
    dl = DLang()
    tmp = dl.compile(codefile)
    if(tmp.ok):
        ags = []
        inp = []
        if args.nargs is not None:
            ags = args.nargs
        if(args.input is not None):
            inputfile = open(args.input, 'r', encoding='utf-8')
            inp = inputfile.read().split()
        dl.run(tmp, ags, inp)
    else:
        if(hasattr(tmp, 'tk')):
            print('Compile error happened, please check the syntax around ' + tmp.tk)
        else:
            print('Compile error: ' + tmp.msg)


if __name__ == '__main__':
    main()
