pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS       = 'ec2-ssh'
        DOCKERHUB_USER        = 'aryansarvaiya13'

        BACK_IMAGE  = 'cloudlab-backend'
        FRONT_IMAGE = 'cloudlab-frontend'

        EC2_HOST = '18.232.35.230'

        BACKEND_DIR  = 'CloudLab-Manager/backend/backend'
        FRONTEND_DIR = 'CloudLab-Manager/frontend'
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Aryan13-tech/DevOps-project.git'
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    // Use withCredentials to login once for both builds
                    withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
                        sh 'echo "$PASS" | docker login -u "$USER" --password-stdin'
                        
                        // Build & Push Backend
                        dir("${BACKEND_DIR}") {
                            sh "docker build -t ${DOCKERHUB_USER}/${BACK_IMAGE}:latest ."
                            sh "docker push ${DOCKERHUB_USER}/${BACK_IMAGE}:latest"
                        }

                        // Build & Push Frontend
                        dir("${FRONTEND_DIR}") {
                            sh "docker build -t ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest ."
                            sh "docker push ${DOCKERHUB_USER}/${FRONT_IMAGE}:latest"
                        }
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            steps {
                echo "🚀 Deploying to EC2..."
                sshagent([SSH_CREDENTIALS]) {
                    // Fix: We pass Jenkins variables into the SSH command properly
                    sh """
                    ssh -o StrictHostKeyChecking=no ubuntu@${EC2_HOST} << 'EOF'
                        set -e
                        
                        # Re-defining variables inside EOF because they don't carry over from Jenkins shell automatically
                        D_USER="${DOCKERHUB_USER}"
                        B_IMG="${BACK_IMAGE}"
                        F_IMG="${FRONT_IMAGE}"

                        echo "🧹 Cleaning up old resources..."
                        docker rm -f cloudlab-backend cloudlab-frontend || true
                        docker image prune -af # Optional: Cleans up old dangling images to save space

                        echo "📥 Pulling latest images..."
                        docker pull \$D_USER/\$B_IMG:latest
                        docker pull \$D_USER/\$F_IMG:latest

                        echo "🚀 Starting containers..."
                        docker run -d --name cloudlab-backend -p 5000:5000 --restart unless-stopped \$D_USER/\$B_IMG:latest
                        docker run -d --name cloudlab-frontend -p 80:80 --restart unless-stopped \$D_USER/\$F_IMG:latest

                        echo "🩺 Health check..."
                        sleep 10
                        curl -f http://localhost:5000/health || (echo 'Backend health check failed' && exit 1)
                        
                        echo "✅ EC2 deployment successful!"
EOF
                    """
                }
            }
        }
    }

    post {
        success { echo "🎉 CI/CD SUCCESS!" }
        failure { echo "❌ CI/CD FAILED!" }
    }
}