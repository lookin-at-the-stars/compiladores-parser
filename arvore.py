class No():
    pass

# Nó Operação Binária (+, -, *, etc)
class NoOperacao(No):
    '''
    Construtor da classe.

    Recebe o tipo de operação e, opcionalmente, os filhos esquerdo e direito.
    Se os filhos esquerdo e direito não forem fornecidos na chamada ao construtor,
    inicializamos com valores padrão (None) só para criar os atributos.
    '''
    def __init__(self, tipo : str, fesq = None, fdir = None):
        self.tipo = tipo
        self.fesq = fesq
        self.fdir = fdir

    # agora, o método avalia recebe tabela de símbolos como parâmetro
    def avalia(self, st : dict):
        valor_esq = self.fesq.avalia(st)
        valor_dir = self.fdir.avalia(st)
        match self.tipo:
            case '+':
                return valor_esq + valor_dir
            case '-':
                return valor_esq - valor_dir
            case '*':
                return valor_esq * valor_dir
            case '/':
                return valor_esq / valor_dir
            case '//':
                return valor_esq // valor_dir

class NoNum(No):
    def __init__(self, valor : int | float):
        self.valor = valor

    def avalia(self, st : dict) -> int | float:
        return self.valor

class NoVar(No):
    def __init__(self, nome : str):
        self.nome = nome

    def avalia(self, st : dict) -> int | float:
        if self.nome not in st:
            raise NameError(f'Variável não definida: {self.nome}')
        return st[self.nome]

class NoAtribui(No):
    def __init__(self, nome : str, expressao):
        self.nome = nome
        self.expressao = expressao

    def avalia(self, st : dict) -> int | float:
        valor = self.expressao.avalia(st)
        st[self.nome] = valor
        return valor

class NoPrint(No):
    def __init__(self, expressao):
        self.expressao = expressao

    def avalia(self, st : dict) -> int | float:
        return self.expressao.avalia(st)