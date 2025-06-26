pipeline {
    agent any

    environment {
    PYTHONIOENCODING = 'utf-8'
    VENV_DIR = 'venv'
    ALLURE_DIR = 'allure-results'

    parameters {
        string(name: 'EXECUTOR', defaultValue: 'selenoid', description: 'Selenoid address (hostname in Docker network)')
        string(name: 'APP_HOST', defaultValue: 'http://host.docker.internal', description: 'App URL')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser')
        string(name: 'BVERSION', defaultValue: '120.0', description: 'Browser version')
        string(name: 'THREADS', defaultValue: '2', description: 'Parallel threads')
    }

    stages {
        stage('Checkout') {
            steps {
              git url: 'https://github.com/Darkmax17/Otus_Docker.git', branch: 'jenkins-support'
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
                allure includeProperties: false, jdk: '',reportBuildPolicy: 'ALWAYS', results: [[path: 'allure-results']]
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'logs/**/*.log', allowEmptyArchive: true
        }
    }
}
