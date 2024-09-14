pipeline {
    agent any
    triggers {
        githubPush()
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'pwd'
                sh 'ls -la'
                sh 'git branch --show-current'
                sh 'git rev-parse HEAD'
            }
        }
        stage('Setup Python Environment') {
            steps {
                sh '''
                    echo "Python version:"
                    python3 --version
                    echo "Pip version:"
                    pip3 --version
                    echo "Installing virtualenv:"
                    pip3 install --user virtualenv --break-system-packages
                    echo "Creating virtual environment:"
                    python3 -m virtualenv venv
                    . venv/bin/activate
                    echo "Installing requirements:"
                    if [ -f Testing/Tree/requirements.txt ]; then
                        pip install -r Testing/Tree/requirements.txt --break-system-package
                    else
                        echo "requirements.txt not found in Testing/Tree/. Please check the file location."
                        exit 1
                    fi
                    echo "Installed packages:"
                    pip list
                '''
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    . venv/bin/activate
                    if [ -f Testing/Tree/tree-testing.py ]; then
                        python3 Testing/Tree/tree-testing.py
                    else
                        echo "tree-testing.py not found in Testing/Tree/. Please check the file location."
                        exit 1
                    fi
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
