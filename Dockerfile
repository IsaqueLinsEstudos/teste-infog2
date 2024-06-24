FROM python:3.9

WORKDIR /app

# Instala o cliente PostgreSQL e os cabeçalhos de desenvolvimento
RUN apt-get update && \
    apt-get install -y postgresql-client libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN python -m venv /opt/venv

# Ativa o ambiente virtual
ENV PATH="/opt/venv/bin:$PATH"

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV PORT=5000

EXPOSE 5000

CMD ["uvicorn", "app.main:app", "--port", "${PORT}"]


