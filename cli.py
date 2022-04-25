import argparse
from dlang import DLang


def main():
    parser = argparse.ArgumentParser(
        description='DLang - DL\'s Lang'
    )
    parser.add_argument('codefile', help='dlang code file')
    parser.add_argument('-a', '--nargs', nargs='+')
    parser.add_argument('-i', '--input')
    parser.add_argument('-m', '--mode')
    args = parser.parse_args()
    codefile = open(args.codefile, 'r', encoding='utf-8')
    mode = 'zh'
    if args.mode is not None:
        mode = args.mode
    dl = DLang(mode)
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
        if(tmp.tk is not None):
            print('Compile error happened, please check the syntax around ' + str(tmp.tk))
        else:
            print('Compile error: ' + tmp.msg)


if __name__ == '__main__':
    main()
