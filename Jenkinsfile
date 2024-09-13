pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/shreyanshdiff/MLops-Kubernetes.git' // Replace with your repository URL
            }
        }
        
        stage('Install Dependencies') {
            steps {
                sh '''
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run Tests') {
            steps {
                sh '''
                # Add any test commands here, e.g., pytest
                pytest
                '''
            }
        }
        
        stage('Build App') {
            steps {
                sh '''
                streamlit run app.py
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: '**/*.pkl', allowEmptyArchive: true
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed!'
        }
    }
}
