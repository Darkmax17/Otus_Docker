pipeline {
  agent any

  parameters {
    string(name: 'APP_URL', defaultValue: 'http://localhost:8080', description: 'Адрес OpenCart')
    string(name: 'SELENOID_URL', defaultValue: 'http://localhost:4444/wd/hub', description: 'Адрес Selenoid')
    string(name: 'BROWSER', defaultValue: 'chrome', description: 'Браузер')
    string(name: 'BROWSER_VERSION', defaultValue: '119.0', description: 'Версия браузера')
    string(name: 'THREADS', defaultValue: '2', description: 'Количество потоков')
  }

  stages {
    stage('Install Python') {
      steps {
        sh '''
          echo "Текущий пользователь: $(whoami)"
          echo "Обновляем apt и ставим python3 и pip..."
          apt-get update || true
          apt-get install -y python3 python3-venv python3-pip || true
        '''
      }
    }

    stage('Install requirements') {
      steps {
        sh '''
          echo "Создание виртуального окружения..."
          python3 -m venv venv
          . venv/bin/activate
          echo "Установка зависимостей..."
          pip install --upgrade pip
          pip install -r requirements.txt
        '''
      }
    }

    stage('Run tests') {
      steps {
        sh '''
          echo "Запуск тестов..."
          . venv/bin/activate
          pytest tests \
            --app-url=$APP_URL \
            --selenoid-url=$SELENOID_URL \
            --browser=$BROWSER \
            --browser-version=$BROWSER_VERSION \
            --alluredir=allure-results \
            -n $THREADS
        '''
      }
    }

    stage('Allure Report') {
      steps {
        allure includeProperties: false, jdk: '', results: [[path: 'allure-results']]
      }
    }
  }
}
