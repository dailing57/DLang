from .ast import *
def functionOverall(value,argList:ArgDefineListASTNode,type,body:StatementListASTNode,rest:RootASTNode):
    body.createContext = True
    fnNode = FunctionASTNode(value,argList,type,body)
    root = RootASTNode()
    root.fns.append(fnNode)
    root.merge(rest)
    return root



