FROM python:3.10-slim

# Установка зависимостей
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    bash \
    wget \
    gnupg \
    curl \
    netcat-traditional\
    && rm -rf /var/lib/apt/lists/*


# Устанавливаем Chrome браузер
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Edge браузер
RUN mkdir -p /etc/apt/keyrings && \
    curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /etc/apt/keyrings/microsoft.gpg && \
    echo "deb [arch=amd64 signed-by=/etc/apt/keyrings/microsoft.gpg] https://packages.microsoft.com/repos/edge stable main" > /etc/apt/sources.list.d/microsoft-edge.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    microsoft-edge-stable \
    && rm -rf /var/lib/apt/lists/*

# Устанавливаем Firefox браузер
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    firefox-esr \
    && rm -rf /var/lib/apt/lists/*

# RUN apt-get update && apt-get install -y --no-install-recommends netcat-traditional

# Рабочая директория
WORKDIR /app

# Установка Python зависимостей
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt


# Копируем код
COPY . .

RUN chmod +x wait-for-it.sh

# Запуск тестов
# ENTRYPOINT ["python", "-m", "pytest"]
CMD []