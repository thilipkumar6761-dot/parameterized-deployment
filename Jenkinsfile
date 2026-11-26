
pipeline {
    agent any

    environment {
        PYTHON = 'C:\\Users\\Thilipkumar\\AppData\\Local\\Python\\bin\\python.exe'
    }

    parameters {
        choice(
            name: 'ENVIRONMENT',
            choices: ['dev', 'staging', 'production'],
            description: 'Select deployment environment'
        )

        string(
            name: 'VERSION',
            defaultValue: '1.0.0',
            description: 'Application version'
        )

        booleanParam(
            name: 'RUN_TESTS',
            defaultValue: true,
            description: 'Run application tests?'
        )

        choice(
            name: 'DEPLOY_REGION',
            choices: ['ap-south-1', 'us-east-1'],
            description: 'Select deployment region'
        )
    }

    stages {

        stage('Checkout Source Code') {
            steps {
                checkout scm
                echo 'Source code checked out successfully'
            }
        }

        stage('Validate Parameters') {
            steps {
                script {
                    if (!(params.ENVIRONMENT in
                        ['dev', 'staging', 'production'])) {
                        error('Invalid environment')
                    }

                    if (!params.VERSION.trim()) {
                        error('Version cannot be empty')
                    }

                    if (!(params.DEPLOY_REGION in
                        ['ap-south-1', 'us-east-1'])) {
                        error('Invalid deployment region')
                    }

                    echo 'All parameters are valid'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                bat '''
                    echo Checking Python...
                    "%PYTHON%" --version

                    "%PYTHON%" -m pip install pytest

                    if exist requirements.txt (
                        "%PYTHON%" -m pip install -r requirements.txt
                    )
                '''
            }
        }

        stage('Run Tests') {
            when {
                expression {
                    return params.RUN_TESTS
                }
            }
            steps {
                bat '''
                    "%PYTHON%" -m pytest test_app.py -v
                '''
            }
        }

        stage('Deploy Application') {
            steps {
                script {

                    def sshCredentialId
                    def deployHost

                    if (params.DEPLOY_REGION == 'ap-south-1') {
                        sshCredentialId = 'mumbai-ec2-key'
                        deployHost = '15.252.137.40'
                    } else {
                        sshCredentialId = 'us-east-ec2-key'
                        deployHost = '98.89.38.181'
                    }

                    withCredentials([
                        sshUserPrivateKey(
                            credentialsId: sshCredentialId,
                            keyFileVariable: 'SSH_KEY',
                            usernameVariable: 'SSH_USER'
                        )
                    ]) {

                        withEnv(["DEPLOY_HOST=${deployHost}"]) {

                            bat '''
                                echo Fixing SSH key permissions...

                                icacls "%SSH_KEY%" /inheritance:r
                                icacls "%SSH_KEY%" /remove:g "*S-1-5-32-545"
                                icacls "%SSH_KEY%" /grant:r "*S-1-5-18:(R)"

                                echo Checking SSH key permissions...
                                icacls "%SSH_KEY%"

                                if not exist app.py (
                                    echo Application file not found
                                    exit /b 1
                                )

                                echo Connecting to AWS EC2...

                                ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -i "%SSH_KEY%" %SSH_USER%@%DEPLOY_HOST% "mkdir -p /opt/parameterized-app/%ENVIRONMENT%/%VERSION%"

                                if errorlevel 1 exit /b 1

                                echo Uploading application...

                                scp -o BatchMode=yes -o StrictHostKeyChecking=accept-new -i "%SSH_KEY%" app.py %SSH_USER%@%DEPLOY_HOST%:/opt/parameterized-app/%ENVIRONMENT%/%VERSION%/app.py

                                if errorlevel 1 exit /b 1

                                echo Application deployed successfully!
                            '''
                        }
                    }
                }
            }
        }

        stage('Deployment Details') {
            steps {
                echo "Environment: ${params.ENVIRONMENT}"
                echo "Version: ${params.VERSION}"
                echo "Tests Enabled: ${params.RUN_TESTS}"
                echo "Region: ${params.DEPLOY_REGION}"

                echo 'Deployment completed on AWS EC2!'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Cloud deployment completed!'
        }

        failure {
            echo 'FAILURE: Cloud deployment failed!'
        }
    }
}
