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
                sh '. venv/bin/activate'
            }
        }

        stage('Run Tests') {
            steps {
                sh '. venv/bin/activate && python tree-testing.py'
            }
        }
    }

    post {
        always {
            cleanWs()
        }
    }
}
