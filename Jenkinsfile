pipeline {
    agent any

    environment {
        // Define the Docker image name and tag for GitHub Packages
        DOCKER_IMAGE = 'ghcr.io/anas-farooq8/flask-calculator-app'
        DOCKER_TAG = 'dev'
        REGISTRY_CREDENTIALS = 'github_credentials' // Jenkins credentials ID for GitHub Package registry
    }

    stages {
        stage('Clone Repository') {
            steps {
                script {
                    git credentialsId: 'github_credentials', branch: 'dev', url: 'https://github.com/NUCES-ISB/assignment-no-2-anas-farooq8'
                }
            }
        }

        stage('Install Python') {
            steps {
                script {
                    // Check if Python3 is installed, install only if not found
                    sh '''
                    if ! which python3 > /dev/null 2>&1; then
                        apt-get update
                        apt-get install -y python3 python3-pip
                        apt install -y python3-pytest
                        apt install -y python3-flask
                    else
                        echo "Python3 is already installed."
                    fi
                    '''
                }
            }
        }

        stage('Run Unit Tests') {
            steps {
                script {
                    sh 'pytest test.py'
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push Docker Image to GitHub Packages') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}", usernameVariable: 'USERNAME', passwordVariable: 'TOKEN')]) {
                        sh """
                        echo $TOKEN | docker login ghcr.io -u $USERNAME --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker environment after the job
            sh 'docker rmi ${DOCKER_IMAGE}:${DOCKER_TAG} || true'
        }
        success {
            echo 'Pipeline completed successfully.'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}