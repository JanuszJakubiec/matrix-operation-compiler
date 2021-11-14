import ply.lex as lex
from tokens import *
from reserved import *


class Scanner(object):
    def __init__(self, **kwargs):
        self.reserved = reserved
        self.tokens = tokens
        self.lexer = lex.lex(module=self, **kwargs)

    # Regular expression rules for simple tokens
    t_PLUS = r'\+'
    t_MINUS = r'-'
    t_TIMES = r'\*'
    t_DIVIDE = r'/'
    t_MAT_PLUS = r'\.\+'
    t_MAT_MINUS = r'\.-'
    t_MAT_TIMES = r'\.\*'
    t_MAT_DIVIDE = r'\./'
    t_ASSIGN = r'='
    t_PLUS_ASSIGN = r'\+='
    t_MINUS_ASSIGN = r'-='
    t_TIMES_ASSIGN = r'\*='
    t_DIVIDE_ASSIGN = r'/='
    t_GREATER = r'>'
    t_LESS = r'<'
    t_GREATER_EQUAL = r'>='
    t_LESS_EQUAL = r'<='
    t_NOT_EQUAL = r'!='
    t_EQUAL = r'=='
    t_L_R_BRACKET = r'\('
    t_R_R_BRACKET = r'\)'
    t_L_S_BRACKET = r'\['
    t_R_S_BRACKET = r'\]'
    t_L_C_BRACKET = r'\{'
    t_R_C_BRACKET = r'\}'
    t_COLON = r':'
    t_TRANSPOSE = r'\''
    t_COMMA = r','
    t_SEMICOLON = r';'

    # rules with action code
    def t_ID(self, t):
        r'[^\W\d]\w*'
        t.type = reserved.get(t.value, 'ID')
        return t

    def t_FLOAT(self, t):
        r'(\d+\.\d*|\.\d+)([eE][\+-]{0,1}\d+){0,1}'
        t.value = float(t.value)
        return t

    def t_INTEGER(self, t):
        r'\d+'
        t.value = int(t.value)
        return t

    def t_STRING(self, t):
        r'"[^\n\"]*"'
        t.value = str(t.value)[1:-1]
        return t

    def t_COMMENT(self, t):
        r'\#.*'
        return

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += len(t.value)
        return

    t_ignore = ' \t\r'

    # Error handling rule
    def t_error(self, t):
        print("Syntax error at line" + str(t.lexer.lineno))
        t.lexer.skip(1)

    def input(self, text):
        return self.lexer.input(text)

    def token(self):
        token = self.lexer.token()
        if token is None: return token
        return "({0}): {1}({2})".format(str(token.lineno), str(token.type), str(token.value))
