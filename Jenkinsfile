pipeline {
agent any

parameters {
    string(name: 'EXECUTOR', defaultValue: 'http://selenoid:4444', description: 'Selenoid address')
    string(name: 'APP_HOST', defaultValue: 'http://app:8080', description: 'App host')
    string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser')
    string(name: 'BVERSION', defaultValue: '121.0', description: 'Browser version')
    string(name: 'THREADS', defaultValue: '2', description: 'Threads')
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
                mkdir -p logs
                . venv/bin/activate
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
