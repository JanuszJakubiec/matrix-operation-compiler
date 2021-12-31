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
    def __init__(self, if_statement, ELSE, body, position):
        self.if_statement = if_statement
        self.ELSE = ELSE
        self.else_body = body
        self.position = position

class IfStatement(Node):
    def __init__(self, sentence, body, position):
        self.sentence = sentence
        self.body = body
        self.position = position

class WhileStatement(Node):
    def __init__(self, sentence, body, position):
        self.sentence = sentence
        self.body = body
        self.position = position

class ForStatement(Node):
    def __init__(self, id, assign, range, body, position):
        self.id = id
        self.assign = assign
        self.range = range
        self.body = body
        self.position = position

class Range(Node):
    def __init__(self, left, right, position):
        self.left = left
        self.right = right
        self.position = position

class Sentence(Node):
    def __init__(self, left, operator, right, position):
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position

class BinaryOperator(Node):
    def __init__(self, left, operator, right, position):
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position

class SingleOperator(Node):
    def __init__(self, operator, expression, position):
        self.operator = operator
        self.expression = expression
        self.position = position

class Assignment(Node):
    def __init__(self, left, operator, right, position):
        self.left = left
        self.operator = operator
        self.right = right
        self.position = position

class MatrixCall(Node):
    def __init__(self, expression, integer1, integer2, position):
        self.expression = expression
        self.x = integer1
        self.y = integer2
        self.position = position

class Return(Node):
    def __init__(self, expression, position):
        self.expression = expression
        self.position = position

class Print(Node):
    def __init__(self, sequence, position):
        self.sequence = sequence
        self.position = position

class InstructionBlock(Node):
    def __init__(self, sequence, position):
        self.sequence = sequence
        self.position = position

class Matrix(Node):
    def __init__(self, rows, position):
        self.rows = rows
        self.position = position

class Row(Node):
    def __init__(self, sequence, position):
        self.position = position
        self.sequence = sequence

class Integer(Node):
    def __init__(self, value, position):
        self.value = value
        self.position = position


class Id(Node):
    def __init__(self, value, position):
        self.value = value
        self.position = position


class Float(Node):
    def __init__(self, value, position):
        self.value = value
        self.position = position


class String(Node):
    def __init__(self, value, position):
        self.value = value
        self.position = position

class Break(Node):
    def __init__(self, position):
        self.position = position

class Continue(Node):
    def __init__(self, position):
        self.position = position

class Eye(Node):
    def __init__(self, function, expression, position):
        self.function = function
        self.expression = expression
        self.position = position

class Zeros(Node):
    def __init__(self, function, expression, position):
        self.function = function
        self.expression = expression
        self.position = position

class Ones(Node):
    def __init__(self, function, expression, position):
        self.function = function
        self.expression = expression
        self.position = position
