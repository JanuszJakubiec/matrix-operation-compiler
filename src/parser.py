import scanner
import ply.yacc as yacc

tokens = scanner.tokens

precedence = (
    # return keyword
    ('left', 'RETURN'),
    # else keyword
    ('right', 'ELSE'),
    # conditionals
    ('right', 'IF', 'WHILE', 'FOR'),
    # function calls
    ('right', 'EYE', 'ZEROS', 'ONES', 'PRINT'),
    # assign operands
    ('right', 'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN'),
    # relation operands
    ('right', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'EQUAL', 'NOT_EQUAL'),
    # number and matrix operands
    ('left', 'PLUS', 'MINUS', 'MAT_PLUS', 'MAT_MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MAT_TIMES', 'MAT_DIVIDE'),
    # brackets operands
    ('right', 'L_R_BRACKET', 'R_R_BRACKET', 'L_S_BRACKET', 'R_S_BRACKET', 'L_C_BRACKET', 'R_C_BRACKET'),
    # colon and comma operand
    ('left', 'COLON', 'COMMA'),
    # transpose operand
    ('left', 'APOSTROPHE'),
    # negation operand
    ('right', 'NOT'),
    # semicolon operand
    ('right', 'SEMICOLON')
)


def p_error(p):
    if p:
        print("Syntax error at line {0}: LexToken({1}, '{2}')".format(p.lineno, p.type, p.value))
    else:
        print("Unexpected end of input")


def p_program(p):
    """program : instructions_opt"""


def p_instructions_opt_1(p):
    """instructions_opt : instructions """


def p_instructions_opt_2(p):
    """instructions_opt : """


def p_instructions_1(p):
    """instructions : instructions instruction """


def p_instructions_2(p):
    """instructions : instruction """


# to finish the grammar
# ....


parser = yacc.yacc()
