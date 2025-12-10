pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS = 'ec2-ssh'
        DOCKERHUB_USER = 'aryansarvaiya13'

        BACK_IMAGE = "cloudlab-backend"
        FRONT_IMAGE = "cloudlab-frontend"

        EC2_HOST = "18.232.35.230"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/Aryan13-tech/DevOps-project.git'
            }
        }

        stage('Build Backend Image') {
            steps {
                script {
                    sh """
                    cd CloudLab-Manager/backend
                    docker build -t ${DOCKERHUB_USER}/${BACK_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                script {
                    sh """
                    cd CloudLab-Manager/frontend
                    docker build -t ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS,
                                                 usernameVariable: 'USER',
                                                 passwordVariable: 'PASS')]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Images to DockerHub') {
            steps {
                script {
                    sh """
                    docker push ${DOCKERHUB_USER}/${BACK_IMAGE}:latest
                    docker push ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest
                    """
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([SSH_CREDENTIALS]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} '
                        docker rm -f cloudlab-backend || true
                        docker rm -f cloudlab-frontend || true

                        docker pull ${DOCKERHUB_USER}/${BACK_IMAGE}:latest
                        docker pull ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest

                        docker run -d --name cloudlab-backend \
                            -p 8000:8000 \
                            -v /var/run/docker.sock:/var/run/docker.sock \
                            ${DOCKERHUB_USER}/${BACK_IMAGE}:latest

                        docker run -d --name cloudlab-frontend \
                            -p 80:80 \
                            ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest
                    '
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🚀 Deployment Successful!"
        }
        failure {
            echo "❌ Deployment Failed!"
        }
    }
}
