# Usa uma imagem leve do Python
FROM python:3.9-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia todo o conteúdo da pasta atual para o container
COPY . /app

# Executa o analisador apontando para o pacote correto
CMD ["python", "-m", "LexerProject.main"]