# Relatório — Parser LL (Descida Recursiva)

## 1. Visão Geral

O parser implementado no projeto é um **parser LL baseado em descida recursiva**, desenvolvido em Python.  
Ele consome tokens produzidos pelo lexer por meio de um `TokenStreamWrapper` e constrói uma **AST (Abstract Syntax Tree)** representada por dicionários Python.

O objetivo do parser é reconhecer um **subconjunto estruturado da linguagem Kotlin**, suficiente para análise estrutural e experimentação com conceitos de compiladores.

---

## 2. Modelo do Parser

### 2.1 Tipo de Parser

- Estratégia: **LL(1)**
- Implementação: **Descida Recursiva**
- Lookahead principal: 1 token
- Controle: funções recursivas que representam regras da gramática

Cada método do parser corresponde a uma produção da gramática, por exemplo:

- `parse_file`
- `parse_declaration`
- `parse_function`
- `parse_property`
- `parse_block`
- `parse_expression`

O fluxo geral é:

1. O parser recebe a sequência de tokens.
2. Analisa conforme a gramática prevista.
3. Constrói uma estrutura hierárquica (AST).
4. Reporta erros sintáticos quando necessário.

---

## 3. O que o Parser Reconhece

O parser cobre as seguintes construções sintáticas:

---

## 3.1 Estrutura de Arquivo

Reconhece:

- `package` (opcional)
- `import`
- Lista de declarações de topo

Formato da AST:

```json
{
  "type": "kotlinFile",
  "package": null | {...},
  "imports": [...],
  "declarations": [...]
}
```

---

## 3.2 Declarações de Topo

- `class`
- `object`
- `fun`
- `val`
- `var`

---

## 3.3 Funções

Reconhece:

- Nome da função  
- Lista de parâmetros  
- Tipo de retorno opcional  
- Corpo delimitado por `{ ... }`

Exemplo reconhecido:

```kotlin
fun soma(a: Int, b: Int): Int {
    return a + b;
}
```

AST simplificada:

```json
{
  "type": "function",
  "name": "soma",
  "params": [...],
  "return": "Int",
  "body": {...}
}
```

---

## 3.4 Propriedades

Reconhece:

- `val` ou `var`
- Nome do identificador
- Tipo opcional (`:`)
- Inicializador opcional (`=`)
- Ponto-e-vírgula obrigatório

Exemplo:

```kotlin
val x = 10;
var y: Int = 20;
```

---

## 3.5 Blocos

Blocos delimitados por `{` e `}` contendo:

- Declarações
- Expressões
- `if`
- `for`

---

## 3.6 Expressões

O parser implementa precedência de operadores através de múltiplas funções encadeadas.

### Ordem de precedência suportada:

1. Elvis (`?:`)
2. OR lógico (`||`)
3. AND lógico (`&&`)
4. Igualdade (`==`, `!=`)
5. Relacional (`<`, `>`, `<=`, `>=`, `in`, `is`)
6. Aditivo (`+`, `-`)
7. Multiplicativo (`*`, `/`, `%`)
8. Unário (`!`, `-`, `++`, `--`)
9. Pós-fixo (`a++`, chamadas, acesso a membros)

Exemplo:

```kotlin
val x = a+++b;
```

Interpretado como:

```
(a++) + b
```

---

## 3.7 Strings

Reconhece:

- Strings normais `"texto"`
- Strings raw `""" texto """`

Interpolação:

- `$identificador`
- `${expressao}`

---

## 3.8 Literais

Suporta:

- Inteiros
- Float
- Hexadecimal
- Binário
- Char
- String

---

## 3.9 Chamadas e Acesso a Membros

- `obj.metodo()`
- `obj.campo`
- Encadeamento múltiplo

---

# 4. Estratégia de Tratamento de Erros

## 4.1 Método `expect()`

Verifica se o próximo token corresponde ao esperado.

Caso contrário:

- Registra erro sintático.
- Ativa mecanismo de recuperação.

---

## 4.2 Recuperação por Panic Mode

Sincroniza em tokens como:

- `;`
- `}`
- `EOF`

Objetivo: permitir que o parser continue e detecte múltiplos erros em uma única execução.

---

# 5. Limitações do Parser

Apesar de funcional, o parser apresenta limitações importantes:

---

## 5.1 Subconjunto da Linguagem

Não implementa completamente:

- `when`
- `try/catch`
- Lambdas completas
- Generics avançados
- Interfaces
- Herança complexa
- Annotations
- Delegação
- Coroutines

---

## 5.2 Exigência de Ponto-e-Vírgula

O parser exige `;` explicitamente ao final das declarações, enquanto Kotlin real permite omissão em muitos casos.

---

## 5.3 Soft Keywords

Palavras como `file`, `get`, `set` podem exigir tratamento especial para serem aceitas como identificadores válidos, dependendo da implementação atual.

---

## 5.4 Ausência de Análise Semântica

O parser:

- Não verifica tipos
- Não valida redeclarações
- Não constrói tabela de símbolos
- Não executa checagem semântica

Ele realiza apenas análise sintática.

---


# 6. Possíveis Melhorias

- Implementar análise semântica
- Suporte a `when`
- Suporte completo a lambdas
- Melhorar recuperação de erros
- Implementar inserção automática de `;`
- Transformar AST em classes ao invés de dicionários
- Expandir cobertura da gramática Kotlin

---

# 7. Conclusão

O parser LL implementado é uma solução sólida para análise sintática de um subconjunto de Kotlin.

Ele:

- Reconhece corretamente estruturas essenciais da linguagem
- Implementa precedência de operadores
- Gera AST consistente
- Possui mecanismo básico de recuperação de erros
