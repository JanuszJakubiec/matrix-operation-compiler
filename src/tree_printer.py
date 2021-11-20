from __future__ import print_function
import matrix_ast
def add_to_class(cls):

    def decorator(func):
        setattr(cls,func.__name__,func)
        return func
    return decorator

def indent_text(string, i):
    out = ""
    for i in range(i):
        out += "|  "
    out += string
    return out

def print_tree_check(variable, indent):
    var_type = type(variable)
    if var_type is str:
        print(indent_text(variable, indent))
        return
    if var_type is int or var_type is float:
        print(indent_text(str(variable), indent))
        return
    variable.print_tree(indent)
    return

class TreePrinter:

    @add_to_class(matrix_ast.Error)
    def print_tree(self, indent=0):
        pass

    @add_to_class(matrix_ast.Program)
    def print_tree(self):
        print("PROGRAM")
        indent = 0
        for element in self.children:
            element.print_tree(indent + 1)

    @add_to_class(matrix_ast.ConditionalStatement)
    def print_tree(self, indent):
        print_tree_check(self.if_statement, indent)
        if self.ELSE:
            print(indent_text("ELSE", indent))
            print_tree_check(self.else_body, indent+1)

    @add_to_class(matrix_ast.IfStatement)
    def print_tree(self, indent):
        print(indent_text("IF", indent))
        print(indent_text("CONDITION", indent + 1))
        print_tree_check(self.sentence, indent+2)
        print(indent_text("BODY", indent + 1))
        print_tree_check(self.body, indent+2)

    @add_to_class(matrix_ast.WhileStatement)
    def print_tree(self, indent):
        print(indent_text("WHILE", indent))
        print(indent_text("CONDITION", indent + 1))
        print_tree_check(self.sentence, indent+2)
        print(indent_text("BODY", indent + 1))
        print_tree_check(self.body, indent+2)

    @add_to_class(matrix_ast.ForStatement)
    def print_tree(self, indent):
        print(indent_text("FOR", indent))
        print(indent_text("EXPRESSION", indent+1))
        print(indent_text(self.assign, indent+2))
        print(indent_text(self.id, indent+3))
        print_tree_check(self.range, indent+3)
        print(indent_text("BODY", indent+1))
        print_tree_check(self.body, indent+2)

    @add_to_class(matrix_ast.Range)
    def print_tree(self, indent):
        print(indent_text("RANGE", indent))
        print_tree_check(self.left, indent+1)
        print_tree_check(self.right, indent+1)

    @add_to_class(matrix_ast.Sentence)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        if self.left != None:
            print_tree_check(self.left, indent+1)
        print_tree_check(self.right, indent+1)

    @add_to_class(matrix_ast.FunctionCall)
    def print_tree(self, indent):
        print(indent_text(self.function, indent))
        print_tree_check(self.expression, indent+1)

    @add_to_class(matrix_ast.BinaryOperator)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        print_tree_check(self.left, indent+1)
        print_tree_check(self.right, indent+1)

    @add_to_class(matrix_ast.SingleOperator)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        print_tree_check(self.expression, indent+1)

    @add_to_class(matrix_ast.Assignment)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        print_tree_check(self.left, indent+1)
        print_tree_check(self.right, indent+1)

    @add_to_class(matrix_ast.MatrixCall)
    def print_tree(self, indent):
        print(indent_text("MATRIX_CALL", indent))
        print_tree_check(self.expression, indent+1)
        print_tree_check(self.x, indent+1)
        print_tree_check(self.y, indent+1)

    @add_to_class(matrix_ast.Return)
    def print_tree(self, indent):
        print(indent_text("RETURN", indent))
        print_tree_check(self.expression, indent+1)

    @add_to_class(matrix_ast.Print)
    def print_tree(self, indent):
        print(indent_text("PRINT", indent))
        for element in self.sequence:
            print_tree_check(element, indent+1)

    @add_to_class(matrix_ast.InstructionBlock)
    def print_tree(self, indent):
        for element in self.sequence:
            print_tree_check(element, indent)

    @add_to_class(matrix_ast.Matrix)
    def print_tree(self, indent):
        print(indent_text("MATRIX", indent))
        for element in self.rows:
            print_tree_check(element, indent+1)

    @add_to_class(matrix_ast.Row)
    def print_tree(self, indent):
        print(indent_text("ROW", indent))
        for element in self.sequence:
            print_tree_check(element, indent+1)
