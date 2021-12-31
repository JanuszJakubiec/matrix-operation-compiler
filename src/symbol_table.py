class VariableSymbol(object):

    def __init__(self, name, type):
        self.name = name
        self.type = type

class SymbolTable(object):

    def __init__(self, parent, name, loop): # parent scope and symbol table name
        self.parent = parent
        self.symbols = {}
        self.name = name
        self.inLoop = loop

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.symbols[name] = symbol
    #

    def get(self, name): # get variable symbol or fundef from <name> entry
        value = self.symbols.get(name, None)
        if value is not None:
            return value
        if self.parent is None:
            return None
        return self.parent.get(name)
    #

    def getParentScope(self):
        return self.parent
    #

    def pushScope(self, name, loop):
        newScope = SymbolTable(self, name, loop)
        return newScope
    #

    def popScope(self):
        return self.parent