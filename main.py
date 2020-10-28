from ply import lex
from ply import yacc

tokens = ["INT", "FLOAT", "PLUS", "IMAGINARY_ID",
          "LP", "RP", "MINUS"]


t_LP = r'\('
t_RP = r'\)'


def t_IMAGINARY_ID(token):
    r'i'
    return token


def t_FLOAT(token):
    r'[0-9]+\.[0-9]+'
    token.value = float(token.value)
    return token


def t_INT(token):
    r'\d+'
    value = token.value
    token.value = int(value)
    return token


t_PLUS = r'\+'
t_MINUS = r'-'

# Define a rule so we can track line numbers


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


 # A string containing ignored characters (spaces and tabs)
t_ignore = ' \t'

# Error handling rule


def t_error(t):
    # print("Illegal character '%s'" % t.value[0])
    print("NEL NO CONOZCO EL TOKEN")
    t.lexer.skip(1)


lexer = lex.lex()
# #######################################################################


def p_calculadora(production):
    '''
    calculadora : complex_number_operations
                | empty
    '''
    print("CALCULADORA", production[1])
    return production


def p_complex_number_operations_plus(production):
    '''
    complex_number_operations : LP complex_number RP  PLUS  LP complex_number RP
    '''
    production[0] = production[2] + production[6]
    return production


def p_complex_number_operations_minus(production):
    '''
    complex_number_operations : LP complex_number RP  MINUS  LP complex_number RP
    '''
    production[0] = production[2] - production[6]
    return production


def p_complex_number(production):
    '''
    complex_number : number PLUS number IMAGINARY_ID
    '''
    production[0] = complex(production[1], production[3])
    return production


def p_complex_number_negative_real(production):
    '''
    complex_number : MINUS number PLUS number IMAGINARY_ID
    '''
    production[0] = complex(-production[2], production[4])
    return production


def p_real_part(production):
    '''
    number : INT 
            | FLOAT
    '''
    production[0] = production[1]
    return production


def p_empty(production):
    '''
    empty : 
    '''
    print("EMPTY")
    return production

#####################################################


def p_error(p):
    print(f"Syntax error at {p.value!r}")


# Build
parser = yacc.yacc()

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    parser.parse(s)
