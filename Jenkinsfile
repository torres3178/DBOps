pipeline {
  agent any

  environment {
    APP_IMAGE = "ci-cd-db-demo:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Build') {
      steps {
        bat 'docker build -t "%APP_IMAGE%" ./app'
      }
    }

    stage('Validate DB scripts') {
      steps {
        bat '''
          docker run --rm ^
  --network=bridge ^
  -v C:/ProgramData/Jenkins/.jenkins/workspace/CICD-DBOps/db/migrations:/flyway/sql ^
  flyway/flyway:10 ^
  -url=jdbc:postgresql://host.docker.internal:5432/app_staging ^
  -user=app ^
  -password=app_pw ^
  -validateMigrationNaming=true info

        '''
      }
    }

    stage('Test') {
      steps {
        bat '''
          docker rm -f ci-test-db || exit 0
          docker run -d --name ci-test-db ^
            -e POSTGRES_USER=test -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=testdb ^
            -p 55432:5432 postgres:16

          REM Wait until DB is ready
          :waitloop
          docker exec ci-test-db pg_isready -U test
          if errorlevel 1 (
            ping -n 2 127.0.0.1 >nul
            goto waitloop
          )

          REM Apply migrations
          docker run --rm --network host ^
            -v C:/ProgramData/Jenkins/.jenkins/workspace/CICD-DBOps/db/migrations:/flyway/sql ^
            flyway/flyway:10 ^
            -url=jdbc:postgresql://127.0.0.1:55432/testdb ^
            -user=test -password=secret migrate
        '''
      }
    }

    stage('Deploy Staging') {
      steps {
        bat 'docker compose -p staging -f docker-compose.staging.yml up -d --build'
      }
    }

    stage('Release Prod') {
      steps {
        script {
          input message: 'Deploy to PROD?', ok: 'Yes, deploy'
        }
        bat 'docker compose -p prod -f docker-compose.prod.yml up -d --build'
      }
    }
  }
}
