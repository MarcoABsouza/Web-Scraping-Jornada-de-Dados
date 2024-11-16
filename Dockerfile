# Usa uma imagem base do Python
FROM python:3.12-slim

# Atualiza o sistema e instala dependências do sistema
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    unzip \
    chromium \
    chromium-driver \
    && apt-get clean

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copia o arquivo de dependências para o diretório de trabalho
COPY requirements.txt .

# Instala as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Define variáveis de ambiente para Selenium/Chrome
ENV PATH="/usr/lib/chromium:/usr/lib/chromium-browser:$PATH" \
    CHROMEDRIVER_PATH="/usr/lib/chromium-driver"
    
# Copia o código da aplicação para o contêiner
COPY . .

# Expõe a porta do PostgreSQL (opcional, caso o banco esteja no mesmo contêiner)
EXPOSE 5432

# Instrução CMD para rodar o aplicativo
CMD ["python", "app.py"]