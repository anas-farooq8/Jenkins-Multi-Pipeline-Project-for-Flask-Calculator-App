pipeline {
    agent any

    environment {
        // Docker image name and GitHub Packages registry credentials
        DOCKER_IMAGE = 'ghcr.io/anas-farooq8/flask-calculator-app'
        DOCKER_TAG = 'dev'
        REGISTRY_CREDENTIALS = 'github_credentials'
    }

    stages {

        stage('Clone Repository') {
            steps {
                script {
                    if (env.GIT_BRANCH == 'dev') { // Ensures this runs only for dev branch
                        git credentialsId: 'github_credentials', branch: 'dev', url: 'https://github.com/NUCES-ISB/assignment-no-2-anas-farooq8'
                    } else {
                        error "This pipeline should only run on the dev branch."
                    }
                }
            }
        }

        stage('Install Python') {
            steps {
                script {
                    sh '''
                    if ! which python3 > /dev/null 2>&1; then
                        apt-get update
                        apt-get install -y python3 python3-pip docker.io python3-pytest python3-flask
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
                        echo \$TOKEN | docker login ghcr.io -u \$USERNAME --password-stdin
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
            // Clean up Docker images after the job
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
