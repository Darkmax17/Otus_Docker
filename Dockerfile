# Базовый образ Jenkins
FROM jenkins/jenkins:lts

# Сразу переход на root, чтобы ставить пакеты и плагины
USER root

# 1) Копируем список плагинов и ставим их
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt
RUN /usr/local/bin/install-plugins.sh < /usr/share/jenkins/ref/plugins.txt

# 2) Устанавливаем Python 3.11, venv и curl/unzip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl unzip && \
    rm -rf /var/lib/apt/lists/*

# 3) Устанавливаем Allure CLI
RUN curl -L -o /tmp/allure.tgz \
      https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz && \
    tar zxvf /tmp/allure.tgz -C /opt && \
    ln -s /opt/allure-2.24.1/bin/allure /usr/bin/allure && \
    rm /tmp/allure.tgz

# Возвращаемся под пользователем Jenkins
USER jenkins
