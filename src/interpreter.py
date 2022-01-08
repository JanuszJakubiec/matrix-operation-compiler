import matrix_ast as matrix_ast
from memory import *
from exceptions import *
from visit import *
import sys
import numpy as np

sys.setrecursionlimit(10000)

binary_operation_table = {}
comparator_table = {}


def size_check(left, right):
    if left[2] == right[2] and left[3] == right[3]:
        return True
    else:
        return False


def size_check_multiplication(left, right):
    if left[3] == right[2]:
        return True
    else:
        return False


def if_left_right_are_matrix_assert_proper_size(left, right, proper_size_check):
    if left[0] == "matrix":
        if right[0] != "matrix":
            print("error objects you are adding are not both matrix type")
            return False
        return proper_size_check(left, right)
    if right[0] == "matrix":
        if left[0] != "matrix":
            print("error objects you are adding are not both matrix type")
            return False
        return proper_size_check(left, right)
    return True


def add(left, right):
    return left + right


def subtract(left, right):
    return left - right


def multiply(left, right):
    return left * right


def multiply_matrix(left, right):
    return left @ right


def divide(left, right):
    return left / right


def normal_add(left, right):
    if not if_left_right_are_matrix_assert_proper_size(left, right, size_check):
        print("error wrong types")
        return None
    if left[0] == "matrix":
        return "matrix", add(left[1], right[1]), left[2], right[3]
    return "scalar", add(left[1], right[1])


def normal_subtract(left, right):
    if not if_left_right_are_matrix_assert_proper_size(left, right, size_check):
        print("error wrong types")
        return None
    if left[0] == "matrix":
        return "matrix", subtract(left[1], right[1]), left[2], right[3]
    return "scalar", subtract(left[1], right[1])


def normal_multiply(left, right):
    if not if_left_right_are_matrix_assert_proper_size(left, right, size_check_multiplication):
        print("error wrong types")
        return None
    if left[0] == "matrix":
        return "matrix", multiply_matrix(left[1], right[1]), left[2], right[3]
    return "scalar", multiply(left[1], right[1])


def normal_divide(left, right):
    return "scalar", divide(left[1], right[1])


def perform_operation(matrix, element, operation):
    new_matrix = np.zeros((matrix[2], matrix[3]))
    for i in range(matrix[2]):
        for j in range(matrix[3]):
            new_matrix[i][j] = operation(matrix[1][i][j], element[1])
    return "matrix", new_matrix, matrix[2], matrix[3]


def matrix_add(left, right):
    if left[0] == "matrix":
        return perform_operation(left, right, add)
    else:
        return perform_operation(right, left, add)


def matrix_subtract(left, right):
    if left[0] == "matrix":
        return perform_operation(left, right, subtract)
    else:
        return perform_operation(right, left, subtract)


def matrix_multiply(left, right):
    if left[0] == "matrix":
        return perform_operation(left, right, multiply)
    else:
        return perform_operation(right, left, multiply)


def matrix_divide(left, right):
    if left[0] == "matrix":
        return perform_operation(left, right, divide)
    else:
        return perform_operation(right, left, divide)


def add_binary_operator(operator, function):
    binary_operation_table[operator] = function


def add_comparator(operator, function):
    comparator_table[operator] = function


def perform_binary_operation(operator, left, right):
    return binary_operation_table.get(operator)(left, right)


def perform_compare_operation(operator, left, right):
    if comparator_table.get(operator)(left, right):
        return "scalar", 1
    return "scalar", 0


def equals(left, right):
    return left[1] == right[1]


def not_equals(left, right):
    return left[1] != right[1]


def greater(left, right):
    return left[1] > right[1]


def less(left, right):
    return left[1] < right[1]


def greater_equals(left, right):
    return left[1] >= right[1]


def less_equals(left, right):
    return left[1] <= right[1]


def convert_assign_type(operation):
    if operation == "+=":
        return "+"
    if operation == "-=":
        return "-"
    if operation == "*=":
        return "*"
    if operation == "/=":
        return "/"


class Interpreter(object):

    def __init__(self):
        self.memory = MemoryStack()

    @on('node')
    def visit(self, node):
        return "not implemented"

    @when(matrix_ast.Program)
    def visit(self, node):
        value = ""
        try:
            for element in node.children:
                value = element.accept(self)
        except ReturnValueException as e:
            return e.value
        return value

    @when(matrix_ast.ConditionalStatement)
    def visit(self, node):
        result = node.if_statement.sentence.accept(self)
        if result[1] > 0:
            self.memory.push()
            try:
                value = node.if_statement.body.accept(self)
                return value
            finally:
                self.memory.pop()
        if node.ELSE:
            self.memory.push()
            try:
                value = node.else_body.accept(self)
                return value
            finally:
                self.memory.pop()
        return None

    @when(matrix_ast.WhileStatement)
    def visit(self, node):
        r = None
        self.memory = self.memory.push()
        while node.sentence.accept(self)[1] > 0:
            try:
                r = node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
        self.memory = self.memory.pop()
        return r

    @when(matrix_ast.ForStatement)
    def visit(self, node):
        r = None
        self.memory = self.memory.push()
        variable = node.id
        for_range = node.range.accept(self)
        for i in for_range:
            self.memory.insert(variable, ("scalar", i))
            try:
                r = node.body.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass
        self.memory = self.memory.pop()
        return r

    @when(matrix_ast.Range)
    def visit(self, node):
        left = node.left.accept(self)[1]
        right = node.right.accept(self)[1]
        return range(left, right)

    @when(matrix_ast.Sentence)
    def visit(self, node):
        left = node.left.accept(self)
        right = node.right.accept(self)
        return perform_compare_operation(node.operator, left, right)

    @when(matrix_ast.BinaryOperator)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return perform_binary_operation(node.operator, r1, r2)

    @when(matrix_ast.SingleOperator)
    def visit(self, node):
        element = node.expression.accept(self)
        if node.operator == "TRANSPOSE":
            return "matrix", np.transpose(element[1]), element[3], element[2]
        if element[0] == "matrix":
            return "matrix", -element[1], element[2], element[3]
        return element[0], -element[1]

    @when(matrix_ast.Assignment)
    def visit(self, node):
        right = node.right.accept(self)
        if node.left.__class__.__name__ == "Id":
            new_value = None
            if node.operator == "=":
                new_value = right
            else:
                new_value = perform_binary_operation(convert_assign_type(node.operator),
                                                     node.left.accept(self),
                                                     right)
            self.memory.insert(node.left.value, new_value)
        else:
            new_value = self.memory.get(node.left.expression.value)
            x = node.left.x.accept(self)[1]
            y = node.left.y.accept(self)[1]
            if node.operator == "=":
                new_value[1][x][y] = right[1]
            else:
                new_value[1][x][y] = perform_binary_operation(convert_assign_type(node.operator),
                                                              node.left.accept(self),
                                                              right)[1]
            self.memory.insert(node.left.expression.value, new_value)

    @when(matrix_ast.MatrixCall)
    def visit(self, node):
        matrix = node.expression.accept(self)[1]
        x = node.x.accept(self)[1]
        y = node.x.accept(self)[1]
        return "scalar", matrix[x][y]

    @when(matrix_ast.Return)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value[1])

    @when(matrix_ast.Print)
    def visit(self, node):
        for element in node.sequence:
            print(element.accept(self)[1])

    @when(matrix_ast.InstructionBlock)
    def visit(self, node):
        val = None
        for element in node.sequence:
            val = element.accept(self)
        return val

    @when(matrix_ast.Matrix)
    def visit(self, node):
        array = None
        for i in range(len(node.rows)):
            if array is None:
                array = node.rows[i].accept(self)
            else:
                array = np.append(array, node.rows[i].accept(self), axis=0)
        return "matrix", array, np.size(array,0), np.size(array, 1)

    @when(matrix_ast.Row)
    def visit(self, node):
        array = np.zeros((1, len(node.sequence)))
        for i in range(len(node.sequence)):
            array[0][i] = node.sequence[i].accept(self)[1]
        return array

    @when(matrix_ast.Integer)
    def visit(self, node):
        return "scalar", node.value

    @when(matrix_ast.Id)
    def visit(self, node):
        return self.memory.get(node.value)

    @when(matrix_ast.Float)
    def visit(self, node):
        return "scalar", node.value

    @when(matrix_ast.String)
    def visit(self, node):
        return "scalar", node.value

    @when(matrix_ast.Break)
    def visit(self, node):
        raise BreakException()

    @when(matrix_ast.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(matrix_ast.Eye)
    def visit(self, node):
        size = node.expression.accept(self)[1]
        matrix = np.zeros((size, size))
        for i in range(0, size):
            matrix[i][i] = 1
        return "matrix", matrix, size, size

    @when(matrix_ast.Zeros)
    def visit(self, node):
        size = node.expression.accept(self)[1]
        return "matrix", np.zeros((size, size)), size, size

    @when(matrix_ast.Ones)
    def visit(self, node):
        size = node.expression.accept(self)[1]
        matrix = np.zeros((size, size))
        for i in range(0, size):
            for j in range(0, size):
                matrix[i][j] = 1
        return "matrix", matrix, size, size


add_binary_operator("+", normal_add)
add_binary_operator("-", normal_subtract)
add_binary_operator("*", normal_multiply)
add_binary_operator("/", normal_divide)
add_binary_operator(".+", matrix_add)
add_binary_operator(".-", matrix_subtract)
add_binary_operator(".*", matrix_multiply)
add_binary_operator("./", matrix_divide)
add_comparator("==", equals)
add_comparator("!=", not_equals)
add_comparator(">=", greater_equals)
add_comparator("<=", less_equals)
add_comparator("<", less)
add_comparator(">", greater)
