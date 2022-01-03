import matrix_ast as ast
from symbol_table import SymbolTable, VariableSymbol

ttype = {}

def add_binary_type(operator, left, right, result):
    operator_dict = ttype.get(operator)
    if operator_dict == None:
        ttype[operator] = {}
        ttype[operator][left] = {}
        ttype[operator][left][right] = result
        return
    left_dict = operator_dict.get(left)
    if left_dict == None:
        ttype[operator][left] = {}
        ttype[operator][left][right] = result
        return
    ttype[operator][left][right] = result

def is_matrix_type(type):
    if type == "matrix_int" or type == "matrix_float":
        return True
    return False

def check_columns(lsize_columns, rsize_columns):
    if lsize_columns == rsize_columns:
        return lsize_columns, True
    if lsize_columns == -1:
        return rsize_columns, True
    if rsize_columns == -1:
        return lsize_columns, True
    return None, False

def check_size_compatibility_and_return_type(lsize_row, lsize_columns, rsize_row, rsize_columns, type):
    if lsize_row == rsize_row:
        value, check_successful = check_columns(lsize_columns, rsize_columns)
        if check_successful:
            return type + "/" + str(lsize_row) + "/" + str(value)
        else:
            return None
    if lsize_row == -1:
        value, check_successful = check_columns(lsize_columns, rsize_columns)
        if check_successful:
            return type + "/" + str(lsize_row) + "/" + str(value)
        else:
            return None
    if rsize_row == -1:
        value, check_successful = check_columns(lsize_columns, rsize_columns)
        if check_successful:
            return type + "/" + str(lsize_row) + "/" + str(value)
        else:
            return None
    return None


def get_binary_type(operator, left, right):
    lsize_row = -2
    rsize_row = -2
    lsize_columns = -2
    rsize_columns = -2
    if "/" in left:
        tab = left.split("/")
        lsize_row = int(tab[1],10)
        lsize_columns = int(tab[2],10)
        left = tab[0]
    if "/" in right:
        tab = right.split("/")
        rsize_row = int(tab[1], 10)
        rsize_columns = int(tab[2], 10)
        right = tab[0]
    if left == "error" or right == "error":
        return "error"

    type_and_size_check = ttype.get(operator, {}).get(left, {}).get(right, None)
    if type_and_size_check == None:
        return None

    type = type_and_size_check[0]
    size_check = type_and_size_check[1]
    if size_check:
        if operator == "*":
            if lsize_columns == rsize_row or lsize_columns == -1 or rsize_row == -1:
                return type + "/" + str(lsize_row) + "/" + str(rsize_columns)
            else:
                return None
        else:
            return check_size_compatibility_and_return_type(lsize_row, lsize_columns, rsize_row, rsize_columns, type)

    if is_matrix_type(left):
        return type + "/" + str(lsize_row) + "/" + str(lsize_columns)
    if is_matrix_type(right):
        return type + "/" + str(rsize_row) + "/" + str(rsize_columns)

    return type

def convert_operator(operator):
    if operator == "+=":
        return "+"
    if operator == "-=":
        return "-"
    if operator == "*=":
        return "*"
    if operator == "/=":
        return "/"
    return ""

def convert(type):
    if type == "int":
        return "float"
    return type

class NodeVisitor(object):

    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)


    def generic_visit(self, node):        # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        else:
            for child in node.children:
                if isinstance(child, list):
                    for item in child:
                        if isinstance(item, ast.Node):
                            self.visit(item)
                elif isinstance(child, ast.Node):
                    self.visit(child)

class TypeChecker(NodeVisitor):

    def visit_Program(self, node):
        self.symbol_table = SymbolTable(None, "global", False)
        for child in node.children:
            self.visit(child)

    def visit_ConditionalStatement(self, node):
        self.visit(node.if_statement)
        self.symbol_table.pushScope(self.symbol_table.name + "ELSE", False)
        self.visit(node.else_body)
        self.symbol_table.popScope()

    def visit_IfStatement(self, node):
        self.symbol_table.pushScope(self.symbol_table.name + "IF", False)
        self.visit(node.sentence)
        self.visit(node.body)
        self.symbol_table.popScope()

    def visit_WhileStatement(self, node):
        self.symbol_table.pushScope(self.symbol_table.name + "WHILE", True)
        self.visit(node.sentence)
        self.visit(node.body)
        self.symbol_table.popScope()

    def visit_ForStatement(self, node):
        self.symbol_table.pushScope(self.symbol_table.name + "FOR", True)
        self.symbol_table.put(node.id, "int")
        self.visit(node.range)
        self.visit(node.body)
        self.symbol_table.popScope()

    def visit_Range(self, node):
        lvalue = self.visit(node.left)
        rvalue = self.visit(node.right)
        if lvalue != rvalue or lvalue != 'int':
            print("Line " + str(node.position) + ": Range value must be int")

    def visit_Sentence(self, node):
        ltype = self.visit(node.left)
        rtype = self.visit(node.right)
        if ltype == "error" or rtype == "error":
            return "error"
        if node.operator == "==":
            return "int"
        if (ltype == rtype or convert(ltype) == convert(rtype)) and "/" not in ltype:
            return "int"
        print("Line " + str(node.position) + ": Illegal compare of types: " + ltype + " " + rtype)
        return "error"

    def visit_BinaryOperator(self, node):
        ltype = self.visit(node.left)     # type1 = node.left.accept(self)
        rtype = self.visit(node.right)    # type2 = node.right.accept(self)
        op    = node.operator

        returnType = get_binary_type(op, ltype, rtype)
        if returnType is None:
            print("Line " + str(node.position) + ": Operator " + op + " can't process operands of types " + ltype + " and " + rtype)
            return 'error'

        return returnType

    def visit_SingleOperator(self, node):
        type = self.visit(node.expression)
        if node.operator == "-":
            if type == "error":
                return "error"
            if type == "int":
                return "int"
            if type == "float":
                return "float"
            if "/" in type:
                tab = type.split("/")
            if is_matrix_type(tab[0]):
                return type
            print("Line " + str(node.expression.position) + ": illegal type: " + type)
            return "error"
        else:
            tab = None
            if "/" in type:
                tab = type.split("/")
                type = tab[0]
            if is_matrix_type(type):
                return type + "/" + tab[2] + "/" + tab[1]
            else:
                print("Line " + str(node.expression.position) + ": illegal type: " + type)
                return "error"

    def visit_Assignment(self, node):
        rtype = self.visit(node.right)
        if rtype == "error":
            return "error"
        if node.operator == "=":
            if node.left.__class__.__name__ == "Id":
                self.symbol_table.put(node.left.value, rtype)
                return None
            else:
                if node.left.__class__.__name__ == "MatrixCall":
                    ltype = self.visit(node.left)
                    if ltype == "error":
                        return "error"
                    if node.left.expression.__class__.__name__ == "Id":
                        type = self.symbol_table.get(node.left.expression.value)
                        rows = -2
                        columns = -2
                        if "/" in type:
                            tab = type.split("/")
                            rows = tab[1]
                            columns = tab[2]
                            type = tab[0]
                        if type == "matrix_int" and rtype == "float":
                            type = self.symbol_table.put(node.left.expression.value, type + "/" + rows + "/" + columns)
                            return None
            print("Line " + str(node.left.position) + ": Cannot assign value to something that is not variable")
            return "error"
        if node.left.__class__.__name__ == "Id":
            ltype = self.visit(node.left)
            returnType = get_binary_type(convert_operator(node.operator), ltype, rtype)
            if returnType is None:
                print("Line " + str(node.position) + ": Operator " + node.operator + " can't process operands of types " + ltype + " and " + rtype)
                return 'error'
            if returnType != "error":
                self.symbol_table.put(node.left.value, rtype)
            return None
        if node.left.__class__.__name__ == "MatrixCall":
            ltype = self.visit(node.left)
            if ltype == "error":
                return "error"
            if node.left.expression.__class__.__name__ == "Id":
                rtype = get_binary_type(convert_operator(node.operator), ltype, rtype)
                type = self.symbol_table.get(node.left.expression.value)
                rows = -2
                columns = -2
                if "/" in type:
                    tab = type.split("/")
                    rows = tab[1]
                    columns = tab[2]
                    type = tab[0]
                if type == "matrix_int" and rtype == "float":
                    self.symbol_table.put(node.left.expression.value, type + "/" + rows + "/" + columns)
                    return None
        print("Line " + str(node.left.position) + ": Cannot assign value to something that is not variable")
        return "error"

    def visit_MatrixCall(self, node):
        type = self.visit(node.expression)
        xtype = self.visit(node.x)
        ytype = self.visit(node.y)
        rows = -2
        columns = -2
        if "/" in type:
            tab = type.split("/")
            rows = int(tab[1], 10)
            columns = int(tab[2], 10)
            type = tab[0]
        if not is_matrix_type(type):
            print("Line " + str(node.position) + ": Type: " + type + " is not Matrix type!")
            return 'error'
        if xtype != "int":
            print("Line " + str(node.x.position) + ": Illegal Matrix call type: " + xtype + " it should be integer!")
            return 'error'
        if ytype != "int":
            print("Line " + str(node.y.position) + ": Illegal Matrix call type: " + ytype + " it should be integer!")
            return 'error'
        if node.x.__class__.__name__ == "Integer":
            if not (node.x.value >= 0 and (node.x.value < rows or rows == -1)):
                print("Line " + str(node.x.position) + ": Matrix index x out of range!")
                return "error"
        if node.y.__class__.__name__ == "Integer":
            if not (node.y.value >= 0 and (node.y.value < columns or columns == -1)):
                print("Line " + str(node.y.position) + ": Matrix index y out of range!")
                return "error"
        if type == "matrix_int":
            return "int"
        else:
            return "float"

    def visit_Return(self, node):
        self.visit(node.expression)
        return None

    def visit_Print(self, node):
        self.visit(node.sequence)
        return None

    def visit_InstructionBlock(self, node):
        for i in node.sequence:
            self.visit(i)
        return None

    def visit_Matrix(self, node):
        type = "row_int"
        size = None
        for row in node.rows:
            element_type = self.visit(row)
            if element_type == "error":
                return "error"
            element_type = element_type.split("/")
            row_size = int(element_type[1], 10)
            element_type = element_type[0]
            if size == None:
                size = row_size
            if row_size != size:
                print("Line " + str(row.position) + ": Matrix rows have different sizes")
                type == "error"
            if element_type == "row_float":
                type = "row_float"
            else:
                if element_type != "row_int":
                    type = "error"
        if type == "error":
            return "error"
        if type == "row_int":
            return "matrix_int" + "/" + str(len(node.rows)) + "/" + str(size)
        return "matrix_float" + "/" + str(len(node.rows)) + "/" + str(size)

    def visit_Row(self, node):
        type = "int"
        for element in node.sequence:
            element_type = self.visit(element)
            if element_type == "float" and type != "error":
                type = "float"
            if element_type != "float" and element_type != "int":
                print("Line " + str(node.position) + ": Illegal type inserted to Row: " + element_type)
                type = "error"
        if type == "error":
            return "error"
        if type == "int":
            return ("row_int" + "/" + str(len(node.sequence)) + "/" + str(1))
        return ("row_float" + "/" + str(len(node.sequence)) + "/" + str(1))



    def visit_Integer(self, node):
        return "int"

    def visit_Float(self, node):
        return "float"

    def visit_Id(self, node):
        idType = self.symbol_table.get(node.value)
        if idType != None:
            return idType
        return "error"

    def visit_String(self, node):
        return "string"

    def visit_Break(self, node):
        if self.symbol_table.inLoop:
            return None

        print("Line " + str(node.position) + ": Illegal usage of BREAK outside of loop")

    def visit_Continue(self, node):
        if self.symbol_table.inLoop:
            return None

        print("Line " + str(node.position) + ": Illegal usage of Continue outside of loop")

    def visit_Eye(self, node):
        type = self.visit(node.expression)
        if type == "int":
            if node.expression.__class__.__name__ == "Integer":
                return "matrix_int" + "/" + str(node.expression.value) + "/" + str(node.expression.value)
            else:
                return "matrix_int/-1/-1"
        else:
            print("Line " + str(node.position) + ": Illegal eye function call. Argument type cannot be " + type)
            return "error"

    def visit_Zeros(self, node):
        type = self.visit(node.expression)
        if type == "int":
            if node.expression.__class__.__name__ == "Integer":
                return "matrix_int" + "/" + str(node.expression.value) + "/" + str(node.expression.value)
            else:
                return "matrix_int/-1/-1"
        else:
            print("Line " + str(node.position) + ": Illegal zeros function call. Argument type cannot be " + type)
            return "error"

    def visit_Ones(self, node):
        type = self.visit(node.expression)
        if type == "int":
            if node.expression.__class__.__name__ == "Integer":
                return "matrix_int" + "/" + str(node.expression.value) + "/" + str(node.expression.value)
            else:
                return "matrix_int/-1/-1"
        else:
            print("Line " + str(node.position) + ": Illegal ones function call. Argument type cannot be " + type)
            return "error"

add_binary_type("+", "int", "int", ("int", False))
add_binary_type("+", "float", "int", ("float", False))
add_binary_type("+", "int", "float", ("float", False))
add_binary_type("+", "float", "float", ("int", False))
add_binary_type("+", "string", "string", ("float", False))
add_binary_type("+", "matrix_int", "matrix_float", ("matrix_float", True))
add_binary_type("+", "matrix_int", "matrix_int", ("matrix_int", True))
add_binary_type("+", "matrix_float", "matrix_int", ("matrix_float", True))
add_binary_type("+", "matrix_float", "matrix_float", ("matrix_float", True))

add_binary_type("-", "int", "int", ("int", False))
add_binary_type("-", "float", "int", ("float", False))
add_binary_type("-", "int", "float", ("float", False))
add_binary_type("-", "float", "float", ("int", False))
add_binary_type("-", "string", "string", ("float", False))
add_binary_type("-", "matrix_int", "matrix_float", ("matrix_float", True))
add_binary_type("-", "matrix_int", "matrix_int", ("matrix_int", True))
add_binary_type("-", "matrix_float", "matrix_int", ("matrix_float", True))
add_binary_type("-", "matrix_float", "matrix_float", ("matrix_float", True))

add_binary_type("*", "int", "int", ("int", False))
add_binary_type("*", "float", "int", ("float", False))
add_binary_type("*", "int", "float", ("float", False))
add_binary_type("*", "float", "float", ("int", False))
add_binary_type("*", "string", "int", ("string", False))
add_binary_type("*", "int", "string", ("string", False))
add_binary_type("*", "matrix_int", "matrix_float", ("matrix_float", True))
add_binary_type("*", "matrix_int", "matrix_int", ("matrix_int", True))
add_binary_type("*", "matrix_float", "matrix_int", ("matrix_float", True))
add_binary_type("*", "matrix_float", "matrix_float", ("matrix_float", True))

add_binary_type("/", "int", "int", ("float", False))
add_binary_type("/", "float", "int", ("float", False))
add_binary_type("/", "int", "float", ("float", False))
add_binary_type("/", "float", "float", ("int", False))

add_binary_type(".+", "matrix_int", "int", ("matrix_int", False))
add_binary_type(".+", "matrix_int", "float", ("matrix_float", False))
add_binary_type(".+", "matrix_float", "int", ("matrix_float", False))
add_binary_type(".+", "matrix_float", "float", ("matrix_float", False))
add_binary_type(".+", "int", "matrix_int", ("matrix_int", False))
add_binary_type(".+", "float", "matrix_int", ("matrix_float", False))
add_binary_type(".+", "int", "matrix_float", ("matrix_float", False))
add_binary_type(".+", "float", "matrix_float", ("matrix_float", False))

add_binary_type(".-", "matrix_int", "int", ("matrix_int", False))
add_binary_type(".-", "matrix_int", "float", ("matrix_float", False))
add_binary_type(".-", "matrix_float", "int", ("matrix_float", False))
add_binary_type(".-", "matrix_float", "float", ("matrix_float", False))

add_binary_type(".*", "matrix_int", "int", ("matrix_int", False))
add_binary_type(".*", "matrix_int", "float", ("matrix_float", False))
add_binary_type(".*", "matrix_float", "int", ("matrix_float", False))
add_binary_type(".*", "matrix_float", "float", ("matrix_float", False))
add_binary_type(".*", "int", "matrix_int", ("matrix_int", False))
add_binary_type(".*", "float", "matrix_int", ("matrix_float", False))
add_binary_type(".*", "int", "matrix_float", ("matrix_float", False))
add_binary_type(".*", "float", "matrix_float", ("matrix_float", False))

add_binary_type("./", "matrix_int", "int", ("matrix_float", False))
add_binary_type("./", "matrix_int", "float", ("matrix_float", False))
add_binary_type("./", "matrix_float", "int", ("matrix_float", False))
add_binary_type("./", "matrix_float", "float", ("matrix_float", False))
