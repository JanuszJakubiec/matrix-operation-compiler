import ply.lex as lex


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
t_APOSTROPHE = r'\''
t_COMMA = r','
t_SEMICOLON = r';'
t_ID = r'[^\W\d]\w*'


def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_FLOAT(t):
    r'\d+\.\d*'
    t.value = float(t.value)
    return t


def t_STRING(t):
    r'".*"'
    t.value = str(t.value)[1:-1]
    return t


def t_COMMENT(t):
    r'#.*'
    return


t_ignore = ' \t\n'


def Scanner():
    pass