pipeline {
  agent any

  environment {
    APP_IMAGE = "ci-cd-db-demo:${env.BUILD_NUMBER}"
  }

  stages {
    stage('Build') {
      steps {
        bat 'docker build -t "$APP_IMAGE" ./app'
      }
    }

    stage('Validate DB scripts') {
      steps {
        bat '''
          docker run --rm \
            -v "$PWD/db/migrations:/flyway/sql" \
            flyway/flyway:10 \
            -validateMigrationNaming=true info
        '''
      }
    }

    stage('Test') {
      steps {
        bat '''
          # Start test DB
          docker rm -f ci-test-db || true
          docker run -d --name ci-test-db \
            -e POSTGRES_USER=test -e POSTGRES_PASSWORD=secret -e POSTGRES_DB=testdb \
            -p 55432:5432 postgres:16
          until docker exec ci-test-db pg_isready -U test; do sleep 1; done

          # Apply migrations
          docker run --rm --network host \
            -v "$PWD/db/migrations:/flyway/sql" \
            flyway/flyway:10 \
            -url=jdbc:postgresql://127.0.0.1:55432/testdb \
            -user=test -password=secret migrate

          # Run tests
          python3 -m venv .venv
          . .venv/bin/activate
          pip install -r app/requirements.txt pytest
          pytest -q
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
