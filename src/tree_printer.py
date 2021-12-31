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
        self.if_statement.print_tree(indent)
        if self.ELSE:
            print(indent_text("ELSE", indent))
            self.else_body.print_tree(indent + 1)

    @add_to_class(matrix_ast.IfStatement)
    def print_tree(self, indent):
        print(indent_text("IF", indent))
        print(indent_text("CONDITION", indent + 1))
        self.sentence.print_tree(indent + 2)
        print(indent_text("BODY", indent + 1))
        self.body.print_tree(indent + 2)

    @add_to_class(matrix_ast.WhileStatement)
    def print_tree(self, indent):
        print(indent_text("WHILE", indent))
        print(indent_text("CONDITION", indent + 1))
        self.sentence.print_tree(indent + 2)
        print(indent_text("BODY", indent + 1))
        self.body.print_tree(indent + 2)

    @add_to_class(matrix_ast.ForStatement)
    def print_tree(self, indent):
        print(indent_text("FOR", indent))
        print(indent_text("EXPRESSION", indent+1))
        print(indent_text(self.assign, indent+2))
        print(indent_text(self.id, indent+3))
        self.range.print_tree(indent + 3)
        print(indent_text("BODY", indent+1))
        self.body.print_tree(indent + 2)

    @add_to_class(matrix_ast.Range)
    def print_tree(self, indent):
        print(indent_text("RANGE", indent))
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @add_to_class(matrix_ast.Sentence)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        if self.left is not None:
            self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @add_to_class(matrix_ast.Zeros)
    def print_tree(self, indent):
        print(indent_text(self.function, indent))
        self.expression.print_tree(indent + 1)

    @add_to_class(matrix_ast.Ones)
    def print_tree(self, indent):
        print(indent_text(self.function, indent))
        self.expression.print_tree(indent + 1)

    @add_to_class(matrix_ast.Eye)
    def print_tree(self, indent):
        print(indent_text(self.function, indent))
        self.expression.print_tree(indent + 1)

    @add_to_class(matrix_ast.BinaryOperator)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @add_to_class(matrix_ast.SingleOperator)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        self.expression.print_tree(indent + 1)

    @add_to_class(matrix_ast.Assignment)
    def print_tree(self, indent):
        print(indent_text(self.operator, indent))
        self.left.print_tree(indent + 1)
        self.right.print_tree(indent + 1)

    @add_to_class(matrix_ast.MatrixCall)
    def print_tree(self, indent):
        print(indent_text("MATRIX_CALL", indent))
        self.expression.print_tree(indent + 1)
        self.x.print_tree(indent + 1)
        self.y.print_tree(indent + 1)

    @add_to_class(matrix_ast.Return)
    def print_tree(self, indent):
        print(indent_text("RETURN", indent))
        self.expression.print_tree(indent + 1)

    @add_to_class(matrix_ast.Print)
    def print_tree(self, indent):
        print(indent_text("PRINT", indent))
        for element in self.sequence:
            element.print_tree(indent + 1)

    @add_to_class(matrix_ast.InstructionBlock)
    def print_tree(self, indent):
        for element in self.sequence:
            element.print_tree(indent)

    @add_to_class(matrix_ast.Matrix)
    def print_tree(self, indent):
        print(indent_text("MATRIX", indent))
        for element in self.rows:
            element.print_tree(indent + 1)

    @add_to_class(matrix_ast.Row)
    def print_tree(self, indent):
        print(indent_text("ROW", indent))
        for element in self.sequence:
            element.print_tree(indent + 1)

    @add_to_class(matrix_ast.Integer)
    def print_tree(self, indent):
        print(indent_text(str(self.value), indent))

    @add_to_class(matrix_ast.Float)
    def print_tree(self, indent):
        print(indent_text(str(self.value), indent))

    @add_to_class(matrix_ast.String)
    def print_tree(self, indent):
        print(indent_text(self.value, indent))

    @add_to_class(matrix_ast.Id)
    def print_tree(self, indent):
        print(indent_text(str(self.value), indent))

    @add_to_class(matrix_ast.Break)
    def print_tree(self, indent):
        print(indent_text("BREAK", indent))

    @add_to_class(matrix_ast.Continue)
    def print_tree(self, indent):
        print(indent_text("CONTINUE", indent))
