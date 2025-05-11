pipeline {
  agent any

  environment {
    // the ID of your Docker Hub credentials in Jenkins
    DOCKERHUB_CREDS = 'dockerhub-credentials'
    // path to your compose file
    COMPOSE_FILE    = 'docker-compose.yml'
  }

  stages {
  stage('Checkout') {
            steps {
                checkout scmGit(branches: [[name: '*/test']], extensions: [], userRemoteConfigs: [[url: 'https://github.com/umerfaro/mlOps_project.git']])
            }
        }

    stage('Build Images') {
      steps {
        echo "Building all services2fa via docker-compose..."
        sh "docker-compose -f ${COMPOSE_FILE} build --pull"
      }
    }

    stage('Push to Docker Hub') {
      steps {
        echo "Pushing all images to Docker Hub..."
        script {
          docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDS) {
            sh "docker-compose -f ${COMPOSE_FILE} push"
          }
        }
      }
    }

    stage('Deploy (optional)') {
      steps {
        echo "Deploying services (docker-compose up)..."
        sh "docker-compose -f ${COMPOSE_FILE} up -d"
      }
    }
  }

  post {
    success {
      emailext(
        to:      'i211185@nu.edu.pk',
        subject: '✅ Docker-Compose Pipeline Succeeded',
        body:    'Your frontend and backend have been built, pushed, and deployed successfully.',
        mimeType: 'text/html'
      )
    }
    failure {
      emailext(
        to:      'i211184@nu.edu.pk',
        subject: '❌ Docker-Compose Pipeline Failed',
        body:    'Something went wrong in the Docker-Compose pipeline. Please check the Jenkins logs.',
        mimeType: 'text/html'
      )
    }
  }
}
