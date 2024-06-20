FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de requisitos para o diretório /app/requirements
COPY requirements.txt /app/requirements/requirements.txt

# Cria um ambiente virtual e instala as dependências
RUN python -m venv /env \
    && /env/bin/pip install --upgrade pip \
    && /env/bin/pip install --no-cache-dir -r /app/requirements/requirements.txt

# Define as variáveis de ambiente
ENV VIRTUAL_ENV /env
ENV PATH /env/bin:$PATH

# Copia o restante do código fonte para o diretório /app no contêiner
COPY . /app

# Exponha a porta 8000 (opcionalmente, você pode ajustar para a porta que sua aplicação está configurada para usar)
EXPOSE 8000

# Comando padrão para iniciar a aplicação utilizando Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
