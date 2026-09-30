from ply import lex, yacc
import sys

tokens = ('INT', 'FLOAT', 'MAIS', 'MENOS', 'VEZES', 'DIV', 'ABRE_PAREN', 'FECHA_PAREN', 'ID', 'ATRIBUI')

t_INT = r'\d+'
t_FLOAT = r'\d+\.\d+'
t_MAIS = r'\+'
t_MENOS = r'\-'
t_VEZES = r'\*'
t_DIV = r'\/'
t_ABRE_PAREN = r'\('
t_FECHA_PAREN = r'\)'
t_ID = r'[a-zA-Z]+'
t_ATRIBUI = r'='

t_ignore = '\t \r\n'

def t_error(token):
    raise Exception('Recebi token inválido.')

# instanciamos o analisador léxico
analisador = lex.lex()

# --------------------------------------------

from arvore import *

# Regras de produção da gramática: funções começadas em "p_"
def p_stmt_expr(prod):
    'stmt : expr'
    prod[0] = prod[1]

def p_stmt_atribui(prod):
    'stmt : ID ATRIBUI expr'
    # criar no prod[0] um objeto do tipo NoAtribui() (que teremos que criar)

def p_expr_mais(prod):
    'expr : expr MAIS termo'
    prod[0] = NoOperacao(tipo='+')
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]

def p_expr_menos(prod):
    'expr : expr MENOS termo'
    prod[0] = NoOperacao(tipo='-')
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]

def p_expr_termo(prod):
    'expr : termo'
    prod[0] = prod[1]

def p_termo_vezes(prod):
    'termo : termo VEZES fator'
    prod[0] = NoOperacao(tipo='*')
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]

def p_termo_div(prod):
    'termo : termo DIV fator'
    prod[0] = NoOperacao(tipo='/')
    prod[0].fesq = prod[1]
    prod[0].fdir = prod[3]

def p_termo_fator(prod):
    'termo : fator'
    prod[0] = prod[1]

def p_fator_int(prod):
    'fator : INT'
    prod[0] = NoNum(valor = int(prod[1]))

def p_fator_float(prod):
    'fator : FLOAT'
    prod[0] = NoNum(valor = float(prod[1]))

def p_fator_parenteses(prod):
    'fator : ABRE_PAREN expr FECHA_PAREN'
    prod[0] = prod[2]

def p_fator_id(prod):
    'fator : ID'
    # criar no prod[0] objeto do tipo NoVar() (precisa ser criado)

def p_error(produção):
    raise SyntaxError('Sintaxe inválida na nossa linguagem!')

print('Digite os statements:')


# ao instanciar o parser, podemos falar qual a variável inicial da gramática
# (mas é opcional porque normalmente ele consegue inferir!)
parser = yacc.yacc(start='stmt')

st = {} # tabela de símbolos é instanciada como dicionário vazio

# lê linha por linha da entrada padrão (stdin)
for linha in sys.stdin:
    try:
        resultado = parser.parse(linha.strip())
        print('Expressão válida! Valor:', resultado.avalia(st))
    except Exception as e:
        print(e)