pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS       = 'ec2-ssh'
        DOCKERHUB_USER       = 'aryansarvaiya13'

        BACK_IMAGE  = 'cloudlab-backend'
        FRONT_IMAGE = 'cloudlab-frontend'

        EC2_HOST = '18.232.35.230'

        BACKEND_DIR  = 'CloudLab-Manager/backend'
        FRONTEND_DIR = 'CloudLab-Manager/frontend'
    }

    stages {

        stage('Checkout Code') {
            steps {
                echo "📥 Checking out code..."
                git branch: 'main',
                    url: 'https://github.com/Aryan13-tech/DevOps-project.git'
            }
        }

        // 🔧 FIX: Ensure Docker CLI exists inside Jenkins container
        stage('Install Docker CLI') {
            steps {
                echo "🐳 Ensuring Docker CLI is installed..."
                sh '''
                if ! command -v docker >/dev/null 2>&1; then
                  echo "Docker not found. Installing..."
                  apt-get update
                  apt-get install -y docker.io
                else
                  echo "Docker already installed"
                fi
                docker --version
                '''
            }
        }

        stage('Build Backend Image') {
            steps {
                echo "🐳 Building backend image..."
                dir("${BACKEND_DIR}") {
                    sh """
                      docker build -t ${DOCKERHUB_USER}/${BACK_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Build Frontend Image') {
            steps {
                echo "🐳 Building frontend image..."
                dir("${FRONTEND_DIR}") {
                    sh """
                      docker build -t ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest .
                    """
                }
            }
        }

        stage('Login to DockerHub') {
            steps {
                echo "🔐 Logging in to DockerHub..."
                withCredentials([
                    usernamePassword(
                        credentialsId: DOCKERHUB_CREDENTIALS,
                        usernameVariable: 'USER',
                        passwordVariable: 'PASS'
                    )
                ]) {
                    sh 'echo $PASS | docker login -u $USER --password-stdin'
                }
            }
        }

        stage('Push Images to DockerHub') {
            steps {
                echo "📤 Pushing images to DockerHub..."
                sh """
                  docker push ${DOCKERHUB_USER}/${BACK_IMAGE}:latest
                  docker push ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest
                """
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo "🚀 Deploying to EC2..."
                sshagent([SSH_CREDENTIALS]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} << 'EOF'
                        set -e

                        echo "🧹 Stopping old containers..."
                        docker rm -f cloudlab-backend || true
                        docker rm -f cloudlab-frontend || true

                        echo "📥 Pulling latest images..."
                        docker pull ${DOCKERHUB_USER}/${BACK_IMAGE}:latest
                        docker pull ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest

                        echo "🚀 Starting backend..."
                        docker run -d --name cloudlab-backend \\
                          -p 5000:5000 \\
                          --restart unless-stopped \\
                          ${DOCKERHUB_USER}/${BACK_IMAGE}:latest

                        echo "🚀 Starting frontend..."
                        docker run -d --name cloudlab-frontend \\
                          -p 80:80 \\
                          --restart unless-stopped \\
                          ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest

                        echo "🩺 Backend health check..."
                        sleep 10
                        curl -f http://localhost:5000/health

                        echo "✅ EC2 deployment successful!"
                    EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🎉 CI/CD PIPELINE SUCCESS — CloudLab deployed to EC2!"
        }

        failure {
            echo "❌ CI/CD PIPELINE FAILED — Check Jenkins logs."
        }

        always {
            echo "🧹 Jenkins pipeline finished."
        }
    }
}
