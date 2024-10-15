pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'anasfarooq/flask-calculator-app'
        // DOCKER_TAG will be set during the pipeline based on parameters
        REGISTRY_CREDENTIALS = 'dockerhub_credentials' // Ensure this matches the credentials ID in Jenkins
    }

    parameters {
        booleanParam(name: 'DEPLOY', defaultValue: false, description: 'Enable deployment to Docker Hub')
        string(name: 'DOCKER_TAG', defaultValue: '', description: 'Docker image tag (only used if DEPLOY is enabled)', trim: true)
    }

    stages {

        stage('Clone Repository') {
            steps {
                script {
                    git credentialsId: 'github_credentials', branch: 'main', url: 'https://github.com/NUCES-ISB/assignment-no-2-anas-farooq8'
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
                    // If DEPLOY is true, ensure DOCKER_TAG is set by the user
                    if (params.DEPLOY && params.DOCKER_TAG?.trim()) {
                        DOCKER_TAG = params.DOCKER_TAG
                    } else {
                        DOCKER_TAG = 'latest' // Default to 'latest' only if not deploying
                    }
                    echo "Building Docker image with tag: ${DOCKER_TAG}"
                    sh "docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} ."
                }
            }
        }

        stage('Push Docker Image to Docker Hub') {
            when {
                expression {
                    return params.DEPLOY // Only push if DEPLOY is true
                }
            }
            steps {
                script {
                    // Ensure DOCKER_TAG is taken from the user if DEPLOY is enabled
                    withCredentials([usernamePassword(credentialsId: "${REGISTRY_CREDENTIALS}", usernameVariable: 'USERNAME', passwordVariable: 'TOKEN')]) {
                        sh """
                        echo \$TOKEN | docker login -u \$USERNAME --password-stdin
                        docker tag ${DOCKER_IMAGE}:${DOCKER_TAG} ${DOCKER_IMAGE}:${DOCKER_TAG}
                        docker push ${DOCKER_IMAGE}:${DOCKER_TAG}
                        """
                    }
                }
            }
        }
    }

    post {
        always {
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
