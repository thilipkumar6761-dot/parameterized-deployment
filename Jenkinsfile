
pipeline {
    agent any

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
            echo Checking Python installation...

            "C:\\Users\\Thilipkumar\\AppData\\Local\\Python\\bin\\python.exe" --version

            "C:\\Users\\Thilipkumar\\AppData\\Local\\Python\\bin\\python.exe" -m pip install pytest

            if exist requirements.txt (
                "C:\\Users\\Thilipkumar\\AppData\\Local\\Python\\bin\\python.exe" -m pip install -r requirements.txt
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
                bat 'python -m pytest test_app.py -v'
            }
        }

        stage('Deploy Application') {
            steps {
                bat '''
                    if not exist app.py (
                        echo Application file not found
                        exit /b 1
                    )

                    if not exist "deploy\\%ENVIRONMENT%" (
                        mkdir "deploy\\%ENVIRONMENT%"
                    )

                    copy /Y app.py "deploy\\%ENVIRONMENT%\\app.py"

                    echo Deployment completed successfully
                '''
            }
        }

        stage('Deployment Details') {
            steps {
                echo "Environment: ${params.ENVIRONMENT}"
                echo "Version: ${params.VERSION}"
                echo "Tests Enabled: ${params.RUN_TESTS}"
                echo "Region: ${params.DEPLOY_REGION}"

                echo 'Deployment pipeline completed!'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Deployment completed!'
        }

        failure {
            echo 'FAILURE: Deployment failed!'
        }
    }
}
