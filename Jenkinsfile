pipeline {
    agent any

    options {
        skipDefaultCheckout(true)
    }

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS       = 'ec2-ssh'
        DOCKERHUB_USER        = 'aryansarvaiya13'

        BACK_IMAGE  = 'cloudlab-backend'
        FRONT_IMAGE = 'cloudlab-frontend'

        EC2_HOST = '3.238.231.19'

        BACKEND_DIR  = 'CloudLab-Manager/backend'
        FRONTEND_DIR = 'CloudLab-Manager/frontend'

        BUILD_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                cleanWs()
                git branch: 'main', url: 'https://github.com/Aryan13-tech/DevOps-project.git'
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    withCredentials([
                        usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')
                    ]) {
                        sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'

                        dir("${BACKEND_DIR}") {
                            sh "docker build -t ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG} ."
                            sh "docker push ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}"
                        }

                        dir("${FRONTEND_DIR}") {
                            sh "docker build -t ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG} ."
                            sh "docker push ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG}"
                        }
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                sshagent([SSH_CREDENTIALS]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} << EOF
                        set -e

                        echo "Pulling latest images..."
                        docker pull ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}
                        docker pull ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG}

                        echo "Stopping old containers..."
                        docker rm -f cloudlab-backend cloudlab-frontend || true

                        echo "Starting backend..."
                        docker run -d --name cloudlab-backend -p 5000:5000 ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}

                        echo "Starting frontend on port 8080..."
                        docker run -d --name cloudlab-frontend -p 8080:80 ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG}

                        sleep 10
                        curl -f http://localhost:5000/health || exit 1

                        echo "Deployment successful!"
EOF
                    """
                }
            }
        }
    }

    post {
        success { echo "🎉 CloudLab CI/CD SUCCESS!" }
        failure { echo "❌ CloudLab CI/CD FAILED!" }
    }
}
