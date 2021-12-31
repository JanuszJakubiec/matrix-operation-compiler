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

def get_binary_type(operator, left, right):
    lsize = -1
    rsize = -1
    if "/" in left:
        tab = left.split("/")
        lsize = int(tab[1],10)
        left = tab[0]
    if "/" in right:
        tab = right.split("/")
        rsize = int(tab[1], 10)
        right = tab[0]
    if lsize != rsize:
        return None
    if left == "error" or right == "error":
        return "error"
    return ttype.get(operator, {}).get(left, {}).get(right, None)

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

#def matrix_type_decide(rtype, ltype, node, table):


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
        if ltype == rtype or convert(ltype) == convert(rtype):
            return "int"
        print("Line " + str(node.position) + ": Comparing types mismatch. Types: " + ltype + " " + rtype)
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
        if node.operator == "-":
            type = self.visit(node.expression)
            if type == "error":
                return "error"
            if type == "int":
                return "int"
            if type == "float":
                return "float"
            print("Line " + str(node.position) + ": illegal type: " + type)
            return "error"
        else:
            print("unimplemented")
            return "error"

    def visit_Assignment(self, node):
        rtype = self.visit(node.right)
        if node.operator == "=":
            if node.left.__class__.__name__ == "Id":
                self.symbol_table.put(node.left.value, rtype)
            else:
                print("unimplemented")
            return None
        if node.left.__class__.__name__ == "Id":
            ltype = self.visit(node.left)
            returnType = get_binary_type(convert_operator(node.operator), ltype, rtype)
            if returnType is None:
                print("Line " + str(node.position) + ": Operator " + node.operator + " can't process operands of types " + ltype + " and " + rtype)
                return 'error'
            if returnType != "error":
                self.symbol_table.put(node.left.value, rtype)
        else:
            print("unimplemented")
        return None

    def visit_MatrixCall(self, node):
        pass

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
            if row_size != size:
                print("Line " + str(node.position) + ": Matrix rows have different sizes")
                type == "error"
            if element_type == "row_float":
                type = "row_float"
            else:
                if element_type != "row_int":
                    type = "error"
        if type == "error":
            return "error"
        if type == "row_int":
            return ("matrix_int" + "/" + str(size))
        return ("matrix_float" + "/" + str(size))

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
            return ("row_int" + "/" + str(len(node.sequence)))
        return ("row_float" + "/" + str(len(node.sequence)))



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
                return ("matrix_int" + "/" + str(node.expression.value))
            else:
                return ("matrix_int" + "/-1")
        else:
            print("Line " + str(node.position) + ": Illegal eye function call. Argument type cannot be " + type)
            return "error"

    def visit_Zeros(self, node):
        type = self.visit(node.expression)
        if type == "int":
            if node.expression.__class__.__name__ == "Integer":
                return ("matrix_int" + "/" + str(node.expression.value))
            else:
                return ("matrix_int" + "/-1")
        else:
            print("Line " + str(node.position) + ": Illegal zeros function call. Argument type cannot be " + type)
            return "error"

    def visit_Ones(self, node):
        type = self.visit(node.expression)
        if type == "int":
            if node.expression.__class__.__name__ == "Integer":
                return ("matrix_int" + "/" + str(node.expression.value))
            else:
                return ("matrix_int" + "/-1")
        else:
            print("Line " + str(node.position) + ": Illegal ones function call. Argument type cannot be " + type)
            return "error"

add_binary_type("+", "int", "int", "int")
add_binary_type("+", "float", "int", "float")
add_binary_type("+", "int", "float", "float")
add_binary_type("+", "float", "float", "int")
add_binary_type("+", "string", "string", "float")

add_binary_type("-", "int", "int", "int")
add_binary_type("-", "float", "int", "float")
add_binary_type("-", "int", "float", "float")
add_binary_type("-", "float", "float", "float")
add_binary_type("-", "string", "string", "string")

add_binary_type("*", "int", "int", "int")
add_binary_type("*", "float", "int", "float")
add_binary_type("*", "int", "float", "float")
add_binary_type("*", "float", "float", "float")
add_binary_type("*", "string", "string", "string")

add_binary_type("/", "int", "int", "float")
add_binary_type("/", "float", "int", "float")
add_binary_type("/", "int", "float", "float")
add_binary_type("/", "float", "float", "float")

add_binary_type(".+", "matrix_int", "matrix_int", "matrix_int")
add_binary_type(".+", "matrix_float", "matrix_int", "matrix_float")
add_binary_type(".+", "matrix_int", "matrix_float", "matrix_float")
add_binary_type(".+", "matrix_float", "matrix_float", "matrix_float")

add_binary_type(".-", "matrix_int", "matrix_int", "matrix_int")
add_binary_type(".-", "matrix_float", "matrix_int", "matrix_float")
add_binary_type(".-", "matrix_int", "matrix_float", "matrix_float")
add_binary_type(".-", "matrix_float", "matrix_float", "matrix_float")

add_binary_type(".*", "matrix_int", "matrix_int", "matrix_int")
add_binary_type(".*", "matrix_float", "matrix_int", "matrix_float")
add_binary_type(".*", "matrix_int", "matrix_float", "matrix_float")
add_binary_type(".*", "matrix_float", "matrix_float", "matrix_float")

add_binary_type("./", "matrix_int", "matrix_int", "matrix_float")
add_binary_type("./", "matrix_float", "matrix_int", "matrix_float")
add_binary_type("./", "matrix_int", "matrix_float", "matrix_float")
add_binary_type("./", "matrix_float", "matrix_float", "matrix_float")
