# Analisador Léxico e sintático - Kotlin

**Trabalho:** Projeto e desenvolvimento de analisadores léxicos e sintáticos para a linguagem de programação Kotlin (Parte 3 e parte 4)  
**Disciplina:** Compiladores  
**Alunos:**
*   Gustavo Silva
*   Matheus Araujo
*   Ricardo Primo

---

## Pré-requisitos

*   **Python 3.8+**
*   **Docker** (Opcional, para execução em container)

---

## Como Rodar o Código (Manualmente)

1.  **Clone o repositório:**
    ```bash
    https://github.com/thiprer497/lexer-and-parser-for-kotlin-language.git
    ```

2.  **Acesse a pasta raiz:**
    É fundamental estar na pasta raiz do projeto (`lexer-and-parser-for-kotlin-language`) e **não** dentro da pasta do pacote (`LexerProject`).
    ```bash
    cd lexer-and-parser-for-kotlin-language
    ```

3.  **Execute o analisador:**
    O arquivo `main.py` agora funciona como uma ferramenta de linha de comando (CLI). Você deve passar o caminho do(s) arquivo(s) `.kt` que deseja analisar.

    **Sintaxe Básica:**
    ```bash
    # Linux / Mac
    python3 -m LexerProject.main <caminho_do_arquivo>

    # Windows
    python -m LexerProject.main <caminho_do_arquivo>
    ```

    **Exemplos de uso:**

    *   **Para ver a ajuda:** (Rode sem argumentos)
        ```bash
        python3 -m LexerProject.main
        ```
    *   **Para rodar o exemplo padrão:**
        ```bash
        python3 -m LexerProject.main exemplos/exemplo.kt
        ```
    *   **Para rodar múltiplos arquivos de uma vez:**
        ```bash
        python3 -m LexerProject.main exemplos/teste.kt exemplos/complexo.kt exemplos/erros.kt exemplos/estruturas.kt
        ```

---

## Como Rodar o Código (Via Docker)

O Docker foi configurado para aceitar arquivos do seu computador através de volumes.

### 1. Configurar o Dockerfile
Certifique-se de que o arquivo `Dockerfile` na raiz tenha o seguinte conteúdo (usando `ENTRYPOINT`):

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Copia todo o projeto para dentro do container
COPY . /app

# Define o ponto de entrada para o módulo Python
ENTRYPOINT ["python", "-m", "LexerProject.main"]

# Argumentos padrão (vazio)
CMD []
```

### 2. Construir a Imagem
```bash
docker build -t kotlin-lexer .
```

### 3. Executar o Container
Para analisar arquivos, você precisa "espelhar" (mount) a sua pasta atual para dentro do Docker.

*   **Usar arquivos locais:**
    ```bash
    docker run --rm kotlin-lexer exemplos/teste.kt exemplos/complexo.kt exemplos/erros.kt exemplos/estruturas.kt
    ```

*   **Linux / Mac / PowerShell:**
    ```bash
    docker run --rm -v "$(pwd):/app" kotlin-lexer exemplos/exemplo.kt
    ```

*   **Windows (CMD clássico):**
    ```bash
    docker run --rm -v "%cd%:/app" kotlin-lexer exemplos/exemplo.kt
    ```

> **Explicação:** O comando `-v` permite que o Docker leia os arquivos da sua pasta `exemplos/` localmente.

---

## Estrutura e Documentação

### Organização de Pastas
*   **`LexerProject/`**: Contém todo o código fonte Python do analisador.
*   **`exemplos/`**: Contém arquivos `.kt` para teste (ex: `exemplo.kt`).

### Descrição dos Módulos

*   **`main.py`**
    *   **CLI (Command Line Interface):** Ponto de entrada do programa. Gerencia argumentos de linha de comando, leitura de arquivos e exibe mensagens de ajuda. Itera sobre os arquivos fornecidos e invoca o Lexer.

*   **`lexer.py`**
    *   **Motor do Analisador léxico:** Percorre o código-fonte caractere por caractere.
    *   Implementa o **Modo Pânico** (recuperação de erros sem abortar a execução).
    *   Realiza conversão de **Valores** (ex: converte string "0xFF" para inteiro `255`).
    *   Suporta *Strings* multilinha (`"""`), interpolação e escapes Unicode.

*   **`tokens.py`**
    *   Define a dataclass `Token` com os campos: `tipo`, `lexema`, `valor` (novo!), `linha` e `coluna`.

*   **`constantes.py`**
    *   "Banco de dados" léxico. Contém dicionários de Operadores, Símbolos e as listas de Palavras-Chave (Hard, Soft e Modifier Keywords) conforme a especificação oficial do Kotlin.

*   **`erros.py`**
    *   Define exceções personalizadas para controle interno, embora o Lexer priorize o tratamento via Modo Pânico na saída padrão.

*   **`utils.py`**
    *   Funções auxiliares para validação de caracteres (hexadecimal, binário) e separadores.

*   **`token_stream.py`**lexer and parser for kotlin language
    *   Abstração para consumo de tokens (buffer), preparando o terreno para a futura implementação do Analisador Sintático (Parser).

*   **`parse_kotlin.py`**lexer and parser for kotlin language
    *   O parser LL(1) consome os tokens do lexer, valida a estrutura sintática essencial da linguagem Kotlin e constrói uma AST hierárquica, com tratamento básico de erros e precedência correta de operadores.
