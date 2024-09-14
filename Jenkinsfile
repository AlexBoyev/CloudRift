pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh 'pip install --user virtualenv --break-system-packages'
                sh 'python3 -m virtualenv venv'
                sh '. venv/bin/activate && pip install -r requirements.txt --break-system-packages'
            }
        }
        stage('Debug Info') {
            steps {
                sh 'pwd'
                sh 'ls -la'
                sh 'which python'
                sh 'python3 --version'
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    pwd
                    ls -la
                    python tree-testing.py
                '''
            }
        }
    }
    post {
        always {
            cleanWs()
        }
    }
}
