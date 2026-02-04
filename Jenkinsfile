pipeline {
    agent any

    environment {
        AWS_REGION = "us-east-1"
        AWS_ACCOUNT_ID = "612069931113"

        PRODUCT_IMAGE = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/product-service"
        ORDER_IMAGE   = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/order-service"
    }

    stages {

        stage('Checkout Source') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/KrishnaDuvvuri/container-automation-project.git'
            }
        }

        stage('AWS ECR Login') {
            steps {
                withCredentials([
                    string(credentialsId: 'aws-access-key', variable: 'AWS_ACCESS_KEY_ID'),
                    string(credentialsId: 'aws-secret-key', variable: 'AWS_SECRET_ACCESS_KEY')
                ]) {
                    sh '''
                    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
                    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
                    aws configure set region $AWS_REGION

                    aws ecr get-login-password --region $AWS_REGION \
                    | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com
                    '''
                }
            }
        }

        stage('Build Product Service Image') {
            steps {
                sh '''
                docker build -t product-service ./product-service
                docker tag product-service:latest $PRODUCT_IMAGE:latest
                '''
            }
        }

        stage('Build Order Service Image') {
            steps {
                sh '''
                docker build -t order-service ./order-service
                docker tag order-service:latest $ORDER_IMAGE:latest
                '''
            }
        }

        stage('Push Images to ECR') {
            steps {
                sh '''
                docker push $PRODUCT_IMAGE:latest
                docker push $ORDER_IMAGE:latest
                '''
            }
        }

        stage('Deploy to EKS') {
            steps {
                sh '''
                aws eks update-kubeconfig --region ap-south-1 --name product-cluster
                kubectl apply -f k8s/
                '''
            }
        }
    }
}
