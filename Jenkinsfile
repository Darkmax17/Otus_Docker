pipeline {
    agent any

    // Параметры джобы:
    // APP_URL      — URL вашего OpenCart (по умолчанию на порту 8082)
    // SELENOID_URL — URL Selenoid (поднимается по сети selenoid:4444)
    // BROWSER      — chrome
    // BROWSER_VERSION — 119.0
    // THREADS      — число параллельных воркеров pytest-xdist
    parameters {
        string(name: 'SELENOID_URL',
               defaultValue: 'http://selenoid:4444/wd/hub',
               description: 'Адрес Selenoid (Remote WebDriver endpoint)')
        string(name: 'APP_URL',
               defaultValue: 'http://localhost:8082',
               description: 'Базовый URL приложения OpenCart')
        string(name: 'BROWSER',
               defaultValue: 'chrome',
               description: 'Имя браузера для тестов')
        string(name: 'BROWSER_VERSION',
               defaultValue: '119.0',
               description: 'Версия браузера')
        string(name: 'THREADS',
               defaultValue: '2',
               description: 'Количество потоков для pytest-xdist')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Python & venv') {
            steps {
                sh '''
                    apt-get update && \
                    apt-get install -y python3 python3-venv python3-pip
                '''
            }
        }

        stage('Create venv & Install deps') {
            steps {
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pytest tests \
                        --app-url=${APP_URL} \
                        --selenoid-url=${SELENOID_URL} \
                        --browser=${BROWSER} \
                        --browser-version=${BROWSER_VERSION} \
                        --alluredir=allure-results \
                        -n ${THREADS}
                '''
            }
        }

        stage('Publish Allure Report') {
            steps {
                allure([
                    includeProperties: false,
                    jdk: '',
                    results: [[path: 'allure-results']]
                ])
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'allure-results/**/*', allowEmptyArchive: true
        }
    }
}
