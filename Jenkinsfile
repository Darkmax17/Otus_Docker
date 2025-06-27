pipeline {
agent { docker { image 'python:3.10' } }

parameters {
    string(name: 'EXECUTOR', defaultValue: 'http://selenoid:4444', description: 'Selenoid address')
    string(name: 'APP_HOST', defaultValue: 'http://app:8080', description: 'Opencart URL')
    string(name: 'BROWSER', defaultValue: 'chrome', description: 'Browser name')
    string(name: 'BVERSION', defaultValue: '121.0', description: 'Browser version')
    string(name: 'THREADS', defaultValue: '2', description: 'Number of parallel threads')
}

stages {
    stage('Checkout') {
        steps {
            checkout scm
        }
    }
stage('Install Python') {
  steps {
    sh '''
      apt-get update
      apt-get install -y python3 python3-venv python3-pip
    '''
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
}