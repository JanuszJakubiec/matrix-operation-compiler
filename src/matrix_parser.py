import matrix_scanner
from matrix_scanner import Scanner
import ply.yacc as yacc
import matrix_ast

scanner = Scanner()

tokens = matrix_scanner.tokens

precedence = (
    # flow control
    ('right', 'IFX'),
    ('nonassoc', 'ELSE'),
    # colon and comma operand
    ('right', 'COLON'),
    # number and matrix operands
    ('left', 'PLUS', 'MINUS', 'MAT_PLUS', 'MAT_MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MAT_TIMES', 'MAT_DIVIDE'),
    ('right', 'UNARY_MINUS'),
    # getting matrix element
    ('nonassoc', 'MAT_ELEMENT'),
    # transpose operand
    ('left', 'TRANSPOSE'),
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


########################################################################
#                               Program                                #
########################################################################

def p_program(p):
    """program : instructions_opt """
    p[0] = matrix_ast.Program(p[1])


def p_instructions_opt(p):
    """instructions_opt : instructions
                        | epsilon """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0]


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]


def p_instruction(p):
    """instruction : expression SEMICOLON
                   | assignment SEMICOLON
                   | command SEMICOLON
                   | conditional_statement
                   | while_statement
                   | for_statement
                   | instruction_block """
    p[0] = p[1]


def p_epsilon(p):
    """epsilon : """
    pass


########################################################################
#                             Flow control                             #
########################################################################

def p_conditional_statement(p):
    """conditional_statement : if_statement ELSE body
                             | if_statement %prec IFX """
    if len(p) > 2:
        p[0] = matrix_ast.ConditionalStatement(if_statement=p[1], ELSE=True, body=p[3], position=p.lineno(1))
    else:
        p[0] = matrix_ast.ConditionalStatement(if_statement=p[1], ELSE=False, body=None, position=p.lineno(1))


def p_if_statement(p):
    """if_statement : IF L_R_BRACKET sentence R_R_BRACKET body """
    p[0] = matrix_ast.IfStatement(sentence=p[3], body=p[5], position=p.lineno(1))


def p_while_statement(p):
    """while_statement : WHILE L_R_BRACKET sentence R_R_BRACKET body """
    p[0] = matrix_ast.WhileStatement(sentence=p[3], body=p[5], position=p.lineno(1))


def p_for_statement(p):
    """for_statement : FOR ID ASSIGN range body """
    p[0] = matrix_ast.ForStatement(id=p[2], assign=p[3], range=p[4], body=p[5], position=p.lineno(1))


def p_body(p):
    """body : instruction """
    p[0] = p[1]


def p_instruction_block(p):
    """instruction_block : L_C_BRACKET instructions_opt R_C_BRACKET """
    p[0] = matrix_ast.InstructionBlock(p[2], position=p.lineno(1))


def p_range(p):
    """range : expression COLON expression """
    p[0] = matrix_ast.Range(left=p[1], right=p[3], position=p.lineno(1))


########################################################################
#                               Sentence                               #
########################################################################

def p_sentence(p):
    """sentence : expression EQUAL expression
                | expression NOT_EQUAL expression
                | expression GREATER expression
                | expression LESS expression
                | expression GREATER_EQUAL expression
                | expression LESS_EQUAL expression """
    if len(p) > 3:
        p[0] = matrix_ast.Sentence(left=p[1], operator=p[2], right=p[3], position=p.lineno(1))
    else:
        p[0] = matrix_ast.Sentence(left=None, operator=p[1], right=p[2], position=p.lineno(1))


########################################################################
#                              Expression                              #
########################################################################

def p_expression(p):
    """expression : expression PLUS expression
                  | expression MINUS expression
                  | expression MAT_PLUS expression
                  | expression MAT_MINUS expression
                  | expression TIMES expression
                  | expression DIVIDE expression
                  | expression MAT_TIMES expression
                  | expression MAT_DIVIDE expression
                  | MINUS expression %prec UNARY_MINUS
                  | expression TRANSPOSE
                  | eye
                  | zeros
                  | ones
                  | L_R_BRACKET expression R_R_BRACKET
                  | changeable
                  | matrix
                  | integer
                  | float
                  | string """
    if len(p) == 4:
        p[0] = matrix_ast.BinaryOperator(left=p[1], operator=p[2], right=p[3], position=p.lineno(2))
    if len(p) == 3:
        if p[1] == "-":
            p[0] = matrix_ast.SingleOperator(operator=p[1], expression=p[2], position=p.lineno(1))
        if p[2] == "'":
            p[0] = matrix_ast.SingleOperator(operator="TRANSPOSE", expression=p[1], position=p.lineno(2))
    if len(p) == 2:
        p[0] = p[1]
        p.set_lineno(0, p.lineno(1))

def p_eye(p):
    """eye : EYE L_R_BRACKET expression R_R_BRACKET"""
    p[0] = matrix_ast.Eye(function=p[1], expression=p[3], position=p.lineno(1))

def p_zeros(p):
    """zeros : ZEROS L_R_BRACKET expression R_R_BRACKET"""
    p[0] = matrix_ast.Zeros(function=p[1], expression=p[3], position=p.lineno(1))

def p_ones(p):
    """ones : ONES L_R_BRACKET expression R_R_BRACKET"""
    p[0] = matrix_ast.Ones(function=p[1], expression=p[3], position=p.lineno(1))

def p_assignment(p):
    """assignment : changeable ASSIGN expression
                  | changeable PLUS_ASSIGN expression
                  | changeable MINUS_ASSIGN expression
                  | changeable TIMES_ASSIGN expression
                  | changeable DIVIDE_ASSIGN expression """
    p[0] = matrix_ast.Assignment(left=p[1], operator=p[2], right=p[3], position=p.lineno(1))

def p_changeable(p):
    """changeable : id
                  | expression L_S_BRACKET expression COMMA expression R_S_BRACKET %prec MAT_ELEMENT """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = matrix_ast.MatrixCall(expression=p[1], integer1=p[3], integer2=p[5], position=p.lineno(2))


def p_integer(p):
    """integer : INTEGER"""
    p[0] = matrix_ast.Integer(p[1], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))


def p_float(p):
    """float : FLOAT"""
    p[0] = matrix_ast.Float(p[1], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))


def p_string(p):
    """string : STRING"""
    p[0] = matrix_ast.String(p[1], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))

def p_id(p):
    """id : ID"""
    p[0] = matrix_ast.Id(p[1], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))


########################################################################
#                               Command                                #
########################################################################

def p_command(p):
    """command : print_command
               | RETURN expression
               | continue
               | break """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = matrix_ast.Return(expression=p[2], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))

def p_break(p):
    """break : BREAK"""
    p[0] = matrix_ast.Break(position = p.lineno(1))
    p.set_lineno(0, p.lineno(1))

def p_continue(p):
    """continue : CONTINUE"""
    p[0] = matrix_ast.Continue(position = p.lineno(1))
    p.set_lineno(0, p.lineno(1))


def p_print_command(p):
    """print_command : PRINT sequence """
    p[0] = matrix_ast.Print(sequence=p[2], position=p.lineno(1))
    p.set_lineno(0, p.lineno(1))


########################################################################
#                               Matrix                                 #
########################################################################

def p_matrix(p):
    """matrix : L_S_BRACKET row_sequence R_S_BRACKET """
    p[0] = matrix_ast.Matrix(p[2], position=p.lineno(1))


def p_row_sequence(p):
    """row_sequence : row COMMA row_sequence
                    | row """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]


def p_row(p):
    """row : L_S_BRACKET sequence R_S_BRACKET """
    p[0] = matrix_ast.Row(p[2], position=p.lineno(2))
    p.set_lineno(0, p.lineno(2))


def p_sequence(p):
    """sequence : expression COMMA sequence
                | expression """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]
    p.set_lineno(0, p.lineno(1))


parser = yacc.yacc()
