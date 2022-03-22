from type import *
class SymbolTable:
    def __init__(self,father = None) -> None:
        self.father:SymbolTable = father
        self.table:dict[str,Variable] = {}

    def add(self,arg:Variable):
        if arg.name in self.table:
            raise Error(f'Variable {arg.name} has been defined')
        else:
            self.table[arg.name] = arg

    def query(self,name:str):
        if name in self.table:
            return self.table[name]
        elif self.father is not None:
            return self.father.query()
        else:
            return None