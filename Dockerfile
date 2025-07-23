################################################
# 1. Берём официальный Jenkins LTS
################################################
FROM jenkins/jenkins:lts

# Меняем на root, чтобы ставить плагины и OS-пакеты
USER root

# 2. Копируем список плагинов и ставим их через новый cli
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# 3. Устанавливаем Python3 и утилиты (curl, unzip), повторяем попытки при сбоях
RUN rm -rf /var/lib/apt/lists/* && \
    apt-get update -o Acquire::Retries=3 && \
    apt-get install -y --no-install-recommends --fix-missing \
      python3 python3-pip python3-venv curl unzip && \
    rm -rf /var/lib/apt/lists/*

# Возвращаемся к Jenkins-пользователю
USER jenkins

# (далее ваши ENTRYPOINT/CMD, если они были)
