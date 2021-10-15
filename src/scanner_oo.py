import ply.lex as lex

tokens = [
    'PLUS',
    'MINUS',
    'MULTIPLICATION',
    'DIVISION'
]

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


def Scanner():
    pass