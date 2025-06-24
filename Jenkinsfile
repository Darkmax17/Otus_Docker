pipeline {
    agent any

    parameters {
        string(name: 'EXECUTOR', defaultValue: '192.168.100.9', description: 'Selenoid host')
        string(name: 'APP_HOST', defaultValue: 'http://opencart', description: 'Opencart URL')
        string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser name')
        string(name: 'BVERSION', defaultValue: '121.0', description: 'Browser version')
        string(name: 'THREADS', defaultValue: '2', description: 'Threads count')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install requirements') {
            steps {
                sh 'python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Run tests') {
            steps {
                sh """
                    source venv/bin/activate
                    pytest -n $THREADS \
                        --browser=$BROWSER \
                        --bv=$BVERSION \
                        --executor=$EXECUTOR \
                        --url=$APP_HOST \
                        --alluredir=allure-results
                """
            }
        }

        stage('Allure report') {
            steps {
                allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
            }
        }
    }
}
