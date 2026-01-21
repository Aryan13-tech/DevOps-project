pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS       = 'ec2-ssh'
        DOCKERHUB_USER        = 'aryansarvaiya13'

        BACK_IMAGE  = 'cloudlab-backend'
        FRONT_IMAGE = 'cloudlab-frontend'

        EC2_HOST = '18.232.35.230'

        BACKEND_DIR  = 'CloudLab-Manager/backand'
        FRONTEND_DIR = 'CloudLab-Manager/frontend'

        BUILD_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Aryan13-tech/DevOps-project.git'
            }
        }

        stage('Backend Sanity Test') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh '''
                    pip install -r requirements.txt
                    echo "✅ Backend dependencies installed"
                    '''
                }
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'

                        // Backend Image
                        dir("${BACKEND_DIR}") {
                            sh "docker build -t ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG} ."
                            sh "docker push ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}"
                        }

                        // Frontend Image
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
                echo "🚀 Deploying to EC2..."
                sshagent([SSH_CREDENTIALS]) {
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} << EOF
                        set -e

                        D_USER="${DOCKERHUB_USER}"
                        B_IMG="${BACK_IMAGE}"
                        F_IMG="${FRONT_IMAGE}"
                        TAG="${BUILD_TAG}"

                        echo "📥 Pulling images..."
                        docker pull \$D_USER/\$B_IMG:\$TAG
                        docker pull \$D_USER/\$F_IMG:\$TAG

                        echo "🛑 Removing old containers..."
                        docker rm -f cloudlab-backend cloudlab-frontend || true

                        echo "🚀 Starting containers..."
                        docker run -d --name cloudlab-backend -p 5000:5000 --restart unless-stopped \$D_USER/\$B_IMG:\$TAG
                        docker run -d --name cloudlab-frontend -p 80:80 --restart unless-stopped \$D_USER/\$F_IMG:\$TAG

                        echo "🩺 Health Check..."
                        sleep 10
                        curl -f http://localhost:5000/health || exit 1

                        echo "✅ CloudLab deployed successfully!"
EOF
                    """
                }
            }
        }
    }

    post {
        success {
            echo "🎉 CloudLab CI/CD SUCCESS!"
        }
        failure {
            echo "❌ CloudLab CI/CD FAILED!"
        }
    }
}
