FROM jenkins/jenkins:lts

USER root

# 1) Копируем плагины и даём права
COPY plugins /usr/share/jenkins/ref/plugins
RUN chown -R jenkins:jenkins /usr/share/jenkins/ref/plugins

# 2) Устанавливаем Python и утилиты
RUN apt-get update && \
    apt-get install -y \
      python3 python3-pip python3-venv \
      curl unzip git && \
    rm -rf /var/lib/apt/lists/*

# 3) Устанавливаем Allure CLI
RUN curl -L -o /tmp/allure.tgz \
      https://github.com/allure-framework/allure2/releases/download/2.24.1/allure-2.24.1.tgz && \
    tar -zxvf /tmp/allure.tgz -C /opt/ && \
    ln -s /opt/allure-2.24.1/bin/allure /usr/bin/allure && \
    rm /tmp/allure.tgz

USER jenkins
