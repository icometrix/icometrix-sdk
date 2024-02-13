pipeline {
    agent {
        label 'tf-deploy'
    }

    stages {
        stage('fetch_latest_code') {
            steps {
                git credentialsId: 'stash-system-user', url: 'http://stash.icometrix.com/scm/bac/icometrix-sdk.git', branch: 'master'
            }
        }

        stage('push_to_github') {
            steps {
                sh '''
                echo "test succeeded"
                '''
            }     
        }
    }
}