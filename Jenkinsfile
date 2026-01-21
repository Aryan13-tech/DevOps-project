pipeline {
    agent any

    environment {
        DOCKERHUB_CREDENTIALS = 'dockerhub-creds'
        SSH_CREDENTIALS       = 'ec2-ssh'
        DOCKERHUB_USER        = 'aryansarvaiya13'

        BACK_IMAGE  = 'cloudlab-backend'
        FRONT_IMAGE = 'cloudlab-frontend'

        EC2_HOST = '18.232.35.230'

        BACKEND_DIR  = 'CloudLab-Manager/backend'
        FRONTEND_DIR = 'CloudLab-Manager/frontend'

        BUILD_TAG = "${env.BUILD_NUMBER}"
    }

    stages {

        stage('Backend Sanity Check') {
            steps {
                dir("${BACKEND_DIR}") {
                    sh '''
                    pip install -r requirements.txt
                    echo "Backend ready"
                    '''
                }
            }
        }

        stage('Build & Push Images') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: DOCKERHUB_CREDENTIALS, usernameVariable: 'USER', passwordVariable: 'PASS')]) {
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
                        docker pull ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}
                        docker pull ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG}

                        docker rm -f cloudlab-backend cloudlab-frontend || true

                        docker run -d --name cloudlab-backend -p 5000:5000 ${DOCKERHUB_USER}/${BACK_IMAGE}:${BUILD_TAG}
                        docker run -d --name cloudlab-frontend -p 80:80 ${DOCKERHUB_USER}/${FRONT_IMAGE}:${BUILD_TAG}

                        sleep 10
                        curl -f http://localhost:5000/health || exit 1
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
