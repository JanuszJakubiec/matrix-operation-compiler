import matrix_scanner
import ply.yacc as yacc

tokens = matrix_scanner.tokens

precedence = (
    # semicolon operand
    ('right', 'SEMICOLON'),
    # flow control
    ('right', 'IF', 'WHILE', 'FOR', 'RETURN', 'CONTINUE', 'BREAK'),
    ('nonassoc', 'ELSE'),
    # colon and comma operand
    ('right', 'COLON', 'COMMA'),
    # assign operands
    ('right', 'ASSIGN', 'PLUS_ASSIGN', 'MINUS_ASSIGN', 'TIMES_ASSIGN', 'DIVIDE_ASSIGN'),
    # sentence operations
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    # relation operands
    ('nonassoc', 'GREATER', 'LESS', 'GREATER_EQUAL', 'LESS_EQUAL', 'EQUAL', 'NOT_EQUAL'),
    # number and matrix operands
    ('left', 'PLUS', 'MINUS', 'MAT_PLUS', 'MAT_MINUS'),
    ('left', 'TIMES', 'DIVIDE', 'MAT_TIMES', 'MAT_DIVIDE'),
    ('right', 'UNARY_MINUS'),
    # getting matrix element
    ('nonassoc', 'MAT_ELEMENT'),
    # transpose operand
    ('left', 'TRANSPOSE'),
    # function calls
    ('right', 'EYE', 'ZEROS', 'ONES', 'PRINT'),
    # brackets operands
    ('right', 'L_R_BRACKET', 'R_R_BRACKET', 'L_S_BRACKET', 'R_S_BRACKET', 'L_C_BRACKET', 'R_C_BRACKET')
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


def p_instructions_opt(p):
    """instructions_opt : instructions
                        | epsilon """


def p_instructions(p):
    """instructions : instructions instruction
                    | instruction """


def p_instruction(p):
    """instruction : expression SEMICOLON
                   | command SEMICOLON
                   | conditional_statement
                   | while_statement
                   | for_statement
                   | instruction_block """


def p_epsilon(p):
    """epsilon : """
    pass


########################################################################
#                             Flow control                             #
########################################################################

def p_conditional_statement(p):
    """conditional_statement : if_statement ELSE body
                             | if_statement %prec IF """


def p_if_statement(p):
    """if_statement : IF L_R_BRACKET sentence R_R_BRACKET body """


def p_while_statement(p):
    """while_statement : WHILE L_R_BRACKET sentence R_R_BRACKET body """


def p_for_statement(p):
    """for_statement : FOR ID ASSIGN range body """


def p_body(p):
    """body : instruction """


def p_instruction_block(p):
    """instruction_block : L_C_BRACKET instructions_opt R_C_BRACKET """


def p_range(p):
    """range : expression COLON expression """


########################################################################
#                               Sentence                               #
########################################################################

def p_sentence(p):
    """sentence : sentence OR sentence
                | sentence AND sentence
                | NOT sentence
                | expression EQUAL expression
                | expression NOT_EQUAL expression
                | expression GREATER expression
                | expression LESS expression
                | expression GREATER_EQUAL expression
                | expression LESS_EQUAL expression """


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
                  | EYE L_R_BRACKET expression R_R_BRACKET
                  | ZEROS L_R_BRACKET expression R_R_BRACKET
                  | ONES L_R_BRACKET expression R_R_BRACKET
                  | L_R_BRACKET expression R_R_BRACKET
                  | assignment
                  | changeable
                  | INTEGER
                  | FLOAT
                  | STRING """


def p_assignment(p):
    """assignment : changeable ASSIGN expression
                  | changeable PLUS_ASSIGN expression
                  | changeable MINUS_ASSIGN expression
                  | changeable TIMES_ASSIGN expression
                  | changeable DIVIDE_ASSIGN expression """


def p_changeable(p):
    """changeable : ID
                  | matrix
                  | expression L_S_BRACKET INTEGER COMMA INTEGER R_S_BRACKET %prec MAT_ELEMENT """

########################################################################
#                               Command                                #
########################################################################

def p_command(p):
    """command : print_command
               | RETURN expression
               | CONTINUE
               | BREAK """


def p_print_command(p):
    """print_command : PRINT sequence """


########################################################################
#                               Matrix                                 #
########################################################################

def p_matrix(p):
    """matrix : L_S_BRACKET row_sequence R_S_BRACKET """


def p_row_sequence(p):
    """row_sequence : row COMMA row_sequence
                    | row """


def p_row(p):
    """row : L_S_BRACKET sequence R_S_BRACKET """


def p_sequence(p):
    """sequence : expression COMMA sequence
                | expression """


parser = yacc.yacc()
