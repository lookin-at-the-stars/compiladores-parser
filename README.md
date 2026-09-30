# Compiladores Parser

Gabriel Barbosa de Souza
Lucas Osório Baldoino

Interpretador de uma linguagem aritmética simples, implementado em Python com
[PLY](https://www.dabeaz.com/ply/). O programa lê o código-fonte do arquivo
`prog.txt`, analisa cada linha e executa seus statements.

## Instalação e execução

```bash
python -m pip install -r requirements.txt
python interpretador.py
```

O arquivo `prog.txt` deve estar na mesma pasta de `interpretador.py`.

## Linguagem suportada

- Números inteiros e reais, por exemplo `10` e `3.14`.
- Operações `+`, `-`, `*`, `/` e `//` (divisão inteira).
- Parênteses para alterar a precedência, como `(2 + 3) * 4`.
- Variáveis e atribuições, como `total = 10 // 3`.
- Variáveis podem ser usadas em expressões, como `dobro = total * 2`.
- `print(expr)` avalia e mostra o valor da expressão na tela.
- Comentários iniciados por `#`, inclusive no final de uma linha.

A precedência é a usual: multiplicações e divisões são avaliadas antes de
adições e subtrações. Apenas statements `print(expr)` mostram valores; linhas
com expressões simples ou atribuições apenas são avaliadas.

Exemplo de `prog.txt`:

```text
# Cálculo de valores
total = 17 // 3
restante = 17 / 3
print(total)
print(restante + 1)
```

Saída:

```text
5
6.666666666666667
```

## Estrutura

- `interpretador.py`: define o lexer, a gramática PLY, a tabela de símbolos e
	executa o arquivo `prog.txt`.
- `arvore.py`: define os nós da árvore sintática e a avaliação das operações,
	números, variáveis, atribuições e comandos `print`.
