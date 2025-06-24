pipeline {
    agent any

    parameters {
        string(name: 'OPENCART_URL', defaultValue: 'http://localhost', description: 'Адрес OpenCart')
        string(name: 'SELENOID_URL', defaultValue: 'http://localhost:4444/wd/hub', description: 'Адрес Selenium/Selenoid')
        choice(name: 'BROWSER', choices: ['chrome', 'firefox'], description: 'Браузер')
        string(name: 'BROWSER_VERSION', defaultValue: '100.0', description: 'Версия браузера')
        string(name: 'THREADS', defaultValue: '2', description: 'Количество потоков')
    }

    environment {
        ALLURE_RESULTS = 'allure-results'
        ALLURE_REPORT = 'allure-report'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/Darkmax17/Otus_Docker.git'
            }
        }

        stage('Install dependencies') {
            steps {
                sh '''
                    pip install -r requirements.txt
                    pip install allure-pytest
                '''
            }
        }

        stage('Run tests') {
            steps {
                sh '''
                    pytest tests/ \
                        --alluredir=${ALLURE_RESULTS} \

