# Use uma imagem base oficial do Python
FROM python:3.12-slim

# Defina o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código da aplicação para o diretório de trabalho do contêiner
COPY . .

# Exponha a porta que a aplicação Django usará
EXPOSE 8000

# Comando para rodar a aplicação
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "gestao_estc.wsgi:application"]

