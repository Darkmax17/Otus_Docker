pipeline {
    agent any

    parameters {
        string(name: 'APP_URL',
               defaultValue: 'http://opencart:80',
               description: 'Адрес Opencart внутри Docker-сети')
        string(name: 'SELENOID_URL',
               defaultValue: 'http://selenoid:4444/wd/hub',
               description: 'Адрес Selenoid WebDriver')
        string(name: 'BROWSER',
               defaultValue: 'chrome',
               description: 'Имя браузера')
        string(name: 'BROWSER_VERSION',
               defaultValue: '119.0',
               description: 'Версия браузера')
        string(name: 'THREADS',
               defaultValue: '2',
               description: 'Количество параллельных потоков xdist')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install requirements') {
            steps {
                sh """
                  python3 -m venv venv
                  . venv/bin/activate
                  pip install --upgrade pip
                  pip install -r requirements.txt
                """
            }
        }

        stage('Run tests') {
            steps {
                sh """
                  . venv/bin/activate
                  pytest tests \
                    --app-url=${APP_URL} \
                    --selenoid-url=${SELENOID_URL} \
                    --browser=${BROWSER} \
                    --browser-version=${BROWSER_VERSION} \
                    --alluredir=allure-results \
                    -n ${THREADS}
                """
            }
        }

        stage('Allure Report') {
            steps {
                // если плагин Allure уже настроен через Global Tool Configuration
                allure includeProperties: false,
                       results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            // соберём артефакты (логи и отчёт) на всякий случай
            archiveArtifacts artifacts: 'allure-results/**', allowEmptyArchive: true
            archiveArtifacts artifacts: 'logs/**/*.log',   allowEmptyArchive: true
        }
    }
}
