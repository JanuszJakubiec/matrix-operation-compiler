class Node(object):
    pass
    def __str__(self):
        return self.print_tree()

class Error(Node):
    def __init__(self):
        pass

class Program(Node):
    def __init__(self, elements):
        self.children = elements

class ConditionalStatement(Node):
    def __init__(self, if_statement, ELSE, body):
        self.if_statement = if_statement
        self.ELSE = ELSE
        self.else_body = body

class IfStatement(Node):
    def __init__(self, sentence, body):
        self.sentence = sentence
        self.body = body

class WhileStatement(Node):
    def __init__(self, sentence, body):
        self.sentence = sentence
        self.body = body

class ForStatement(Node):
    def __init__(self, id, assign, range, body):
        self.id = id
        self.assign = assign
        self.range = range
        self.body = body

class Range(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right

class Sentence(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class FunctionCall(Node):
    def __init__(self, function, expression):
        self.function = function
        self.expression = expression

class BinaryOperator(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class SingleOperator(Node):
    def __init__(self, operator, expression):
        self.operator = operator
        self.expression = expression

class Assignment(Node):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

class MatrixCall(Node):
    def __init__(self, expression, integer1, integer2):
        self.expression = expression
        self.x = integer1
        self.y = integer2

class Return(Node):
    def __init__(self, expression):
        self.expression = expression

class Print(Node):
    def __init__(self, sequence):
        self.sequence = sequence

class InstructionBlock(Node):
    def __init__(self, sequence):
        self.sequence = sequence

class Matrix(Node):
    def __init__(self, rows):
        self.rows = rows

class Row(Node):
    def __init__(self, sequence):
        self.sequence = sequence

class Integer(Node):
    def __init__(self, value):
        self.value = value


class Id(Node):
    def __init__(self, value):
        self.value = value


class Float(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value
