import ply.lex as lex

verbs = ['undo','redo','ids','show','modify','add','do','delete']

tokens = ('VERB',
    'ID_SPEC',
    'ATOM',
    'IMPLIES',
    'COLON',
    'SEMICOLON')

t_VERB = '^(' + '|'.join(verbs) + ')'
t_ID_SPEC = r'\d+(-\d+)?(,\d+(-\d+)?)*'
t_ATOM = r'(\w+|".*"|\'.*\')'
t_IMPLIES = r'->'
t_COLON = r':'
t_SEMICOLON = r';'
t_ignore = ' \t'

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)


'''
# some tests
lexer = lex.lex()
test_data = ['add scheduled:today;',
    'modify this -> that',
    'show 1',
    'show 2-3',
    'show 2-3,4',
    'show 2-3,5-6',
    'show 2-5,6,8-9',
    'modify this -> "how now?"',
    "modify 'how now brown cow!' -> that"]
for d in test_data:
    lexer.input(d)
    print d
    for tok in lexer:
        print '\t' + str(tok)
'''

import ply.yacc as yacc

# to get the token map from the lexer
from calclex import tokens

def p_empty(p):
    'empty :'
    pass

def p_statement(p):
    'STATEMENT : VERB FILTER
               | VERB FILTER IMPLIES KV
               '

def p_filter(p):
    'FILTER : ID_SPEC FILTER
            | KV FILTER
            | empty'''

def p_kv(p):
    'KV : ATOM COLON ATOM'

def p_error(t):
    print("Syntax error at '%s'" % t.value)


# this goes at the call site
parser = yacc.yacc()
parser.parse(input_string)

