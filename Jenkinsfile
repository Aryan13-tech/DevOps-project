pipeline {
    agent any

    environment {
        APP_NAME = "cloudlab-manager"
        BACKEND_DIR = "CloudLab-Manager/backend"
        FRONTEND_DIR = "CloudLab-Manager/frontend"
        DOCKERHUB_USER = "aryansarvaiya13"
        DOCKERHUB_BACKEND = "cloudlab-backend"
        DOCKERHUB_FRONTEND = "cloudlab-frontend"
    }

    stages {

        stage('Pull Code From GitHub') {
            steps {
                echo "Pulling latest project code..."
                checkout scm
            }
        }

        stage('Cleanup Old Docker Containers') {
            steps {
                sh '''
                echo "Stopping old containers..."
                docker stop cloudlab_backend || true
                docker stop cloudlab_frontend || true

                echo "Removing old containers..."
                docker rm cloudlab_backend || true
                docker rm cloudlab_frontend || true

                echo "Removing old images..."
                docker rmi $DOCKERHUB_USER/$DOCKERHUB_BACKEND:latest || true
                docker rmi $DOCKERHUB_USER/$DOCKERHUB_FRONTEND:latest || true
                '''
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                echo "Building backend image..."
                docker build -t $DOCKERHUB_USER/$DOCKERHUB_BACKEND:latest "$BACKEND_DIR"

                echo "Building frontend image..."
                docker build -t $DOCKERHUB_USER/$DOCKERHUB_FRONTEND:latest "$FRONTEND_DIR"
                '''
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                    sh '''
                    echo "$PASS" | docker login -u "$USER" --password-stdin
                    '''
                }
            }
        }

        stage('Push Images to DockerHub') {
            steps {
                sh '''
                docker push $DOCKERHUB_USER/$DOCKERHUB_BACKEND:latest
                docker push $DOCKERHUB_USER/$DOCKERHUB_FRONTEND:latest
                '''
            }
        }

        stage('Deploy Containers') {
            steps {
                sh '''
                docker run -d --name cloudlab_backend -p 8000:8000 $DOCKERHUB_USER/$DOCKERHUB_BACKEND:latest
                docker run -d --name cloudlab_frontend -p 80:80 $DOCKERHUB_USER/$DOCKERHUB_FRONTEND:latest
                '''
            }
        }
    }

    post {
        success {
            echo "Deployment Success!"
        }
        failure {
            echo "Deployment Failed — Check Jenkins logs."
        }
    }
}
