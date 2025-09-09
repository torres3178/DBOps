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
