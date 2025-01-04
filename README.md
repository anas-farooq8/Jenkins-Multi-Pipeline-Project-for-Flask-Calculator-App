# Jenkins Multi-Pipeline Project for Flask Calculator App

This branch contains the implementation of a Jenkins multi-pipeline for a Flask calculator application. The pipeline includes steps for cloning a GitHub repository, installing dependencies, running unit tests, building a Docker image, and pushing the image to GitHub Packages.

## Overview of Steps

1. **Jenkins Multi-Pipeline Setup**:

   - Created a multi-pipeline project in Jenkins to automate the build and deployment process.
   - Integrated Personal Access Token (PAT) authentication for secure access to GitHub Packages.

2. **Flask Application Development**:
   - Developed a simple Flask application that performs basic arithmetic operations.
   - Created a Dockerfile for containerizing the Flask application.

- create virtual environment using
  `python -m venv .venv`

- source this environment
  `Set-ExecutionPolicy -ExecutionPolicy Bypass -Scope Process`
  `.\.venv\Scripts\Activate.ps1`

- Install all the dependencies
  `pip install -r requirements.txt`

- Test the application
  `pytest test.py`

- Build the docker image
  `docker build -t anas-farooq8/flask-calculator-app .`

- Run the Docker image
  `docker run -d -p 5001:5001 anas-farooq8/flask-calculator-app`

- You can open go into the docker container
  `docker exec -it -u 0 <containerid> /bin/bash`

- Exposing the Jenkins using ngrok
  `ngrok http 8080`

3. **Webhook Configuration**:

   - Set up a webhook in the GitHub repository to trigger the Jenkins pipeline on code changes.

4. **Jenkins Pipeline Configuration**:

   - Run the Jenkins Container:

   ```bash
   docker run --user root -p 8080:8080 -p 5000:5000 -v jenkins_home:/var/jenkins_home -v /var/run/docker.sock:/var/run/docker.sock -d jenkins/jenkins:lts
   ```

   - Configured the Jenkins pipeline as follows:

   ```groovy
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
                           apt-get install -y docker.io
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
   ```
