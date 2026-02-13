# Analisador Léxico - Kotlin

Trabalho: Projeto e desenvolvimento de analisadores léxicos e sintáticos para a linguagem de programação Kotlin (Parte 3)

Disciplina: Compiladores

Alunos:
* Gustavo Silva
* Matheus Araujo
* Ricardo Primo

## Pré- requisitos
* Python 3.8+
* Docker (Opcional para execução em container)

## Como Rodar o Código (Manualmente)

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/thiprer497/lexer_kotlin_python.git
    ```

2.  **Acesse a pasta raiz:** 
    É fundamental estar na pasta raiz do projeto (`lexer_kotlin_python`) e não dentro da pasta do pacote (`LexerProject`).
    ```bash
    cd lexer_kotlin_python
    ```

3.  **Execute o módulo:**
    Utilize a flag `-m` para executar o pacote como um script. Isso garante que as importações relativas funcionem corretamente.

    **Linux / Mac:**
    ```bash
    python3 -m LexerProject.main  
    ```

    **Windows:**
    ```bash
    python -m LexerProject.main 
    ```
    > **Nota:** O ponto de entrada (Main) está no arquivo `main.py`. Ao executar, ele processará o código de exemplo (`sample`) contido no final do arquivo e exibirá os tokens no terminal.

## Como Rodar o Código (Via Docker)

Se preferir rodar em um ambiente isolado, siga os passos abaixo.

### 1. Criar o Dockerfile
Certifique-se de que existe um arquivo chamado `Dockerfile` na raiz do projeto (`lexer_kotlin_python`) com o seguinte conteúdo:

```dockerfile
# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todo o conteúdo da pasta atual para o container
COPY . /app

# Executa o analisador apontando para o pacote correto
CMD ["python", "-m", "LexerProject.main"]
```

### 2. Construir a Imagem
No terminal, na raiz do projeto, execute:

```bash
docker build -t kotlin-lexer .
```

### 3. Rodar o Container
Após a construção, execute o container:

```bash
docker run --rm kotlin-lexer
```

---

## Documentação dos Arquivos

Abaixo segue a descrição da responsabilidade de cada módulo do projeto:

*   **`constantes.py`**
    *   Contém a "base de dados" da gramática léxica. Define os dicionários de mapeamento para Operadores (ex: `+` -> `OP_PLUS`), Símbolos (ex: `(` -> `LPAREN`) e as listas de Palavras-Chave (*Keywords*) classificadas em Rígidas (Hard), Suaves (Soft) e Modificadoras, conforme a especificação oficial do Kotlin.

*   **`tokens.py`**
    *   Define a estrutura de dados `Token` (uma *dataclass*). É o objeto que representa a unidade mínima de significado, armazenando o tipo do token, o lexema (texto original), a linha e a coluna onde foi encontrado.

*   **`erros.py`**
    *   Define as classes de exceção personalizadas para erros léxicos, como `UnclosedComment` (comentário não fechado), `UnclosedString` (string não fechada) e `InvalidCharLiteral`, permitindo um tratamento de erros mais granular e mensagens precisas.

*   **`utils.py`**
    *   Conjunto de funções auxiliares e predicados para verificação de caracteres, como `eh_hex` (verifica hexadecimal), `eh_bin` (binário), e verificadores de sufixos numéricos (`L`, `f`, `u`). Ajuda a manter o código do Lexer limpo e legível.

*   **`lexer.py`**
    *   O coração do analisador léxico. Contém a classe `Lexer`, que percorre o código-fonte caractere por caractere. Implementa a máquina de estados que decide, com base no caractere atual, qual método de reconhecimento acionar (números, strings, identificadores, comentários ou operadores). Gerencia a contagem de linhas e colunas.

*   **`token_stream.py`**
    *   Uma abstração acima do Lexer. Recebe a lista de tokens gerada e fornece métodos para o futuro Analisador Sintático (Parser) consumir esses tokens sequencialmente, como `next()` (consome), `peek()` (espia o próximo sem consumir) e `expect()` (valida se o próximo token é do tipo esperado).

*   **`main.py`**
    *   Arquivo principal de execução. Contém uma string de código Kotlin de teste (cobrindo casos de borda como Shebang, comentários aninhados e literais complexos) e aciona o Lexer, imprimindo a sequência de tokens encontrados no console.

*   **`__init__.py`**
    *   Arquivo que transforma o diretório `LexerProject` em um pacote Python, exportando as classes principais (`Lexer`, `Token`, `TokenStream`) para facilitar a importação.