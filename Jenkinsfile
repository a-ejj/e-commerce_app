pipeline {
    agent any

    triggers {
        githubPush()
    }

    stages {
        stage('Build') {
            steps {
                sh 'python3 -m venv venv'
                // Hem sanal ortamı aktive et hem de bağımlılıkları kur
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                sh '''
                # Sanal ortamı aktive et
                . venv/bin/activate

                # Proje kök dizinini (WORKSPACE) PYTHONPATH'e ekle
                # Bu, Python'ın ana uygulama dosyasını (app.py) bulmasını sağlar
                export PYTHONPATH="${WORKSPACE}:\$PYTHONPATH"

                # Testleri çalıştır
                pytest tests/
                '''
            }
        }
    }
}
