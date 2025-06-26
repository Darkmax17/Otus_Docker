pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR', defaultValue: 'selenoid', description: 'Selenoid address (hostname in Docker network)')
        string(name: 'APP_HOST', defaultValue: 'http://host.docker.internal', description: 'App URL')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser')
        string(name: 'BVERSION', defaultValue: '121.0', description: 'Browser version')
        string(name: 'THREADS', defaultValue: '2', description: 'Parallel threads')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install requirements') {
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
                    mkdir -p logs
                    pytest -n ${THREADS} \
                        --browser=${BROWSER} \
                        --bv=${BVERSION} \
                        --executor=${EXECUTOR} \
                        --url=${APP_HOST} \
                        --alluredir=allure-results \
                        -o log_cli=true -o log_cli_level=INFO
                '''
            }
        }

        stage('Allure Report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/**/*.log', allowEmptyArchive: true
        }
    }
}
