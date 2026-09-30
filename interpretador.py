from ply import lex, yacc

tokens = ('INT', 'FLOAT', 'MAIS', 'MENOS', 'VEZES', 'DIV_INT', 'DIV',
          'ABRE_PAREN', 'FECHA_PAREN', 'ID', 'ATRIBUI', 'PRINT')

reserved = {'print': 'PRINT'}

t_INT = r'\d+'
t_FLOAT = r'\d+\.\d+'
t_MAIS = r'\+'
t_MENOS = r'\-'
t_VEZES = r'\*'
t_DIV_INT = r'//'
t_DIV = r'\/'
t_ABRE_PAREN = r'\('
t_FECHA_PAREN = r'\)'
t_ATRIBUI = r'='

t_ignore = '\t \r\n'

def t_COMMENT(token):
    r'\#[^\n]*'
    pass

def t_ID(token):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    token.type = reserved.get(token.value, 'ID')
    return token

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
    prod[0] = NoAtribui(prod[1], prod[3])

def p_stmt_print(prod):
    'stmt : PRINT ABRE_PAREN expr FECHA_PAREN'
    prod[0] = NoPrint(prod[3])

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

def p_termo_div_int(prod):
    'termo : termo DIV_INT fator'
    prod[0] = NoOperacao(tipo='//')
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
    prod[0] = NoVar(prod[1])

def p_error(producao):
    raise SyntaxError('Sintaxe inválida na nossa linguagem!')

# ao instanciar o parser, podemos falar qual a variável inicial da gramática
# (mas é opcional porque normalmente ele consegue inferir!)
parser = yacc.yacc(start='stmt', write_tables=False, debug=False)

st = {} # tabela de símbolos é instanciada como dicionário vazio

with open('prog.txt', encoding='utf-8') as programa:
    for numero, linha in enumerate(programa, start=1):
        if not linha.strip() or linha.lstrip().startswith('#'):
            continue
        try:
            resultado = parser.parse(linha)
            if isinstance(resultado, NoPrint):
                print(resultado.avalia(st))
            else:
                resultado.avalia(st)
        except Exception as e:
            print(f'Linha {numero}: {e}')