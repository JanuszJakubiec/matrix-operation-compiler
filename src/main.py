import sys
import matrix_scanner  # matrix_scanner.py is a file you create, (it is not an external library)
import matrix_parser
from tree_printer import TreePrinter
from type_checker import TypeChecker
from interpreter import Interpreter

if __name__ == '__main__':

    mode = 'type_check'
#    mode = 'interpreter'
#    mode = 'print_tree'
#    mode = 'scan'
#    mode = 'parse'

    #name of the file to be read
    program = 'example11.m'

    if mode == 'scan':
        try:
            filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
            file = open(filename, "r")
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        text = file.read()
        lexer = matrix_scanner.Scanner()

        # Give the lexer some input
        lexer.input(text)

        # Tokenize
        while True:
            tok = lexer.token()
            if not tok:
                break  # No more input
            print(tok)

    if mode == 'parse':
        try:
            filename = sys.argv[1] if len(sys.argv) > 1 else program
            file = open(filename, "r")
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        parser = matrix_parser.parser
        text = file.read()
        parser.parse(text, lexer=matrix_scanner.Scanner())

    if mode == 'print_tree':
        try:
            filename = sys.argv[1] if len(sys.argv) > 1 else program
            file = open(filename, "r")
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        parser = matrix_parser.parser
        text = file.read()
        ast = parser.parse(text, lexer=matrix_scanner.Scanner())
        ast.print_tree()

    if mode == 'type_check':
        try:
            filename = sys.argv[1] if len(sys.argv) > 1 else program
            file = open(filename, "r")
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        parser = matrix_parser.parser
        text = file.read()
        ast = parser.parse(text, lexer=matrix_scanner.Scanner())
        # Below code shows how to use visitor
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

    if mode == "interpreter":
        try:
            filename = sys.argv[1] if len(sys.argv) > 1 else program
            file = open(filename, "r")
        except IOError:
            print("Cannot open {0} file".format(filename))
            sys.exit(0)

        parser = matrix_parser.parser
        text = file.read()
        ast = parser.parse(text, lexer=matrix_scanner.Scanner())
        typeChecker = TypeChecker()
        typeChecker.visit(ast)  # or alternatively ast.accept(typeChecker)

        interpreter = Interpreter()
        print(ast.accept(interpreter))
