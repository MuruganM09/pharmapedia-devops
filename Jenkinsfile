pipeline {
    agent any
    
    environment {
        ECR_REPO = "541765610657.dkr.ecr.ap-south-1.amazonaws.com/pharmapedia"
        AWS_REGION = "ap-south-1"
        CLUSTER_NAME = "pharmapedia-cluster"
    }
    
    stages {
        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/MuruganM09/pharmapedia-devops.git'
            }
        }
        
        stage('Build Docker Image') {
            steps {
                sh "docker build -t pharmapedia:${BUILD_NUMBER} ./Pharmapedia-an-RAG-assistant-main/Pharmapedia"
            }
        }
        
        stage('Push to ECR') {
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials', 
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID', 
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${ECR_REPO}
                        docker tag pharmapedia:${BUILD_NUMBER} ${ECR_REPO}:${BUILD_NUMBER}
                        docker tag pharmapedia:${BUILD_NUMBER} ${ECR_REPO}:latest
                        docker push ${ECR_REPO}:${BUILD_NUMBER}
                        docker push ${ECR_REPO}:latest
                    """
                }
            }
        }
        
        stage('Deploy to EKS') {
            steps {
                withCredentials([aws(credentialsId: 'aws-credentials',
                                    accessKeyVariable: 'AWS_ACCESS_KEY_ID',
                                    secretKeyVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                    sh """
                        aws eks update-kubeconfig --region ${AWS_REGION} --name ${CLUSTER_NAME}
                        kubectl set image deployment/pharmapedia-app pharmapedia=${ECR_REPO}:${BUILD_NUMBER}
                    """
                }
            }
        }
    }
}