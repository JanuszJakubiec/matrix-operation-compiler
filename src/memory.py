class Memory:

    def __init__(self):  # memory name
        self.variables = {}

    def has_key(self, name):  # variable name
        variable = self.variables.get(name, None)
        if variable == None:
            return False
        return True

    def get(self, name):  # gets from memory current value of variable <name>
        variable = self.variables.get(name, None)
        return variable

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.variables[name] = value


class MemoryStack:

    def __init__(self,parent=None):  # initialize memory stack with memory <memory>
        self.parent = parent
        self.memory = Memory()

    def get(self, name):  # gets from memory stack current value of variable <name>
        if self.memory.has_key(name):
            return self.memory.get(name)
        if self.parent != None:
            return self.parent.get(name)
        else:
            print("NOT DECLARED!")
            return None

    def insert(self, name, value): # put variable symbol or fundef under <name> entry
        inserted = False
        if self.memory.get(name) is None:
            if self.parent is not None:
                inserted = self.parent.insert_parent(name, value)
        if not inserted:
            self.memory.put(name, value)

    def insert_parent(self, name, value):
        if self.memory.get(name) is None:
            if self.parent is None:
                return False
            return self.parent.insert_parent(name, value)
        self.memory.put(name, value)
        return True

    def set(self, name, value):  # sets variable <name> to value <value>
        self.memory.put(name, value)

    def push(self):  # pushes memory <memory> onto the stack
        newMemory = MemoryStack(self)
        return newMemory

    def pop(self):  # pops the top memory from the stack
        return self.parent
