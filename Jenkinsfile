pipeline {
    agent {
        label 'backend-docker-build'
    }

    stages {
        stage('fetch_latest_code') {
            steps {
                git credentialsId: 'stash-system-user', url: 'http://stash.icometrix.com/scm/bac/icometrix-sdk.git', branch: 'master'
            }
        }

        stage('push_to_github') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'gh_icogitadmin', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh '''
                    git push https://$USERNAME:$PASSWORD@github.com/icometrix/icometrix-sdk.git    
                    '''
                }
            }     
        }
    }
}