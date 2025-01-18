# Base image
FROM python:3.12-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Instala dependências do sistema necessárias
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && apt-get clean

# Instala o Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

# Copia os arquivos de configuração do Poetry
COPY poetry.lock pyproject.toml /app/

# Instala as dependências do projeto
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copia o restante do projeto
COPY . .

# Expõe a porta usada pelo Django
EXPOSE 8001

# Comando para iniciar o servidor
CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8001"]