pipeline {
  agent any

  environment {
    // Jenkins credential ID for Docker Hub (username+password)
    DOCKERHUB_CREDS = 'dockerhub-credentials'
    // path to your compose file
    COMPOSE_FILE    = 'docker-compose.yaml'
  }

  stages {
    stage('Checkout') {
      steps {
        // checkout your test branch
        checkout scmGit(
          branches: [[name: '*/test']],
          extensions: [],
          userRemoteConfigs: [[url: 'https://github.com/umerfaro/mlOps_project.git']]
        )
      }
    }

    stage('Build Images') {
      steps {
        echo "🛠 Building backend & frontend images via docker-compose..."
        bat "docker-compose -f %COMPOSE_FILE% build --pull"
      }
    }

    stage('Push to Docker Hub') {
      steps {
        echo "📤 Pushing images to Docker Hub..."
        script {
          docker.withRegistry('https://registry.hub.docker.com', DOCKERHUB_CREDS) {

            echo "pushing images to docker hub again"

          }
        }
      }
    }

    stage('Deploy (optional)') {
      steps {
        echo "🚀 Deploying containers (docker-compose up -d)..."
        bat "docker-compose -f %COMPOSE_FILE% up -d"
      }
    }
  }

  post {
    success {
      emailext(
        to:      'i211185@nu.edu.pk',
        subject: '✅ Docker-Compose Pipeline Succeeded',
        body:    'Your backend and frontend images were built, pushed, and deployed successfully.',
        mimeType:'text/html'
      )
    }
    failure {
      emailext(
        to:      'i211184@nu.edu.pk',
        subject: '❌ Docker-Compose Pipeline Failed',
        body:    'Something went wrong in the Docker-Compose pipeline. Please check the Jenkins logs.',
        mimeType:'text/html'
      )
    }
  }

}
