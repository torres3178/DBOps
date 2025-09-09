pipeline {
  agent any

  environment {
    APP_IMAGE = "ci-cd-db-demo:${env.BUILD_NUMBER}"
    DB_URL = "jdbc:postgresql://localhost:5432/app_staging"
    DB_USER = "app"
    DB_PASSWORD = "app_pw"
  }

  stages {
    stage('Build') {
      steps {
        bat 'docker build -t "%APP_IMAGE%" ./app'
      }
    }

    stage('Validate DB Scripts') {
      steps {
        bat '''
          docker run --rm ^
            -v "%CD%\\db\\migration:/flyway/sql" ^
            flyway/flyway:10 ^
            -url=%DB_URL% ^
            -user=%DB_USER% ^
            -password=%DB_PASSWORD% ^
            -validateMigrationNaming=true ^
            info
        '''
      }
    }

    stage('Run DB Migrations') {
      steps {
        bat '''
          docker run --rm ^
            -v "%CD%\\db\\migration:/flyway/sql" ^
            flyway/flyway:10 ^
            -url=%DB_URL% ^
            -user=%DB_USER% ^
            -password=%DB_PASSWORD% ^
            migrate
        '''
      }
    }

    stage('Deploy Staging') {
      steps {
        bat '''
          docker compose -p staging -f docker-compose.staging.yml up -d --build
        '''
      }
    }

    stage('Release Prod') {
      steps {
        script {
          input message: 'Deploy to PROD?', ok: 'Yes, deploy'
        }
        bat '''
          docker compose -p prod -f docker-compose.prod.yml up -d --build
        '''
      }
    }
  }
}
