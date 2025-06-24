pipeline {
    agent any

    parameters {
        string(name: 'OPENCART_URL', defaultValue: 'http://localhost:8081', description: 'OpenCart URL')
        string(name: 'SELENOID_URL', defaultValue: 'http://localhost:4444/wd/hub', description: 'Selenoid URL')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '120.0', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '2', description: 'Количество потоков')
    }

    environment {
        PYTHONUNBUFFERED = 1
    }

    stages {
        stage('Клонируем проект') {
            steps {
                git 'https://github.com/Darkmax17/Otus_Docker'
            }
        }

        stage('Установка зависимостей') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Запуск автотестов') {
            steps {
                sh '''
                pytest --browser $BROWSER \
                       --version $BROWSER_VERSION \
                       --threads $THREADS \
                       --selenoid $SELENOID_URL \
                       --url $OPENCART_URL \
                       --alluredir=allure-results
                '''
            }
        }

        stage('Формирование отчёта Allure') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }
}
