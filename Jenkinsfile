pipeline {
    agent any // Pipeline'ın herhangi bir Jenkins agent'ında çalışacağını belirtir

    triggers {
        githubPush() // Git deposuna push yapıldığında pipeline'ı otomatik başlatır
    }

    stages {
        stage('Checkout SCM') {
            steps {
                echo 'Checking out code from SCM'
                // Kodunuzu Git deposundan çeker
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application (Setting up virtual environment and installing dependencies)'
                // Sanal Python ortamını oluştur ve aktive et
                sh 'python3 -m venv venv'
                // Sanal ortamı aktive et ve gereksinimleri kur
                // && işareti, önceki komut başarılı olursa sonrakini çalıştırır
                sh '. venv/bin/activate && pip install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests'
                // Sanal ortamı aktive et
                // PYTHONPATH'i ayarla ki testler uygulama modülünü bulabilsin
                // Testleri çalıştır
                sh '''
                . venv/bin/activate
                export PYTHONPATH="${WORKSPACE}:\$PYTHONPATH"
                pytest tests/
                '''
            }
        }

        // --- SonarQube Scanner Kurulum Aşaması ---
        // NOT: Eğer Jenkins Agent'ınızda SonarQube Scanner belirli bir versiyonuyla kalıcı olarak kuruluysa
        // ve PATH'inizde erişilebilir durumdaysa bu aşamayı atlayabilirsiniz.
        // Ancak, ortamın tutarlılığı ve kontrolü için pipeline içinde kurmak genellikle daha iyidir.
        stage('Setup SonarQube Scanner') {
            steps {
                echo "Setting up SonarQube Scanner"
                // SonarQube Scanner versiyonunu belirle (SonarQube sunucunuzla uyumlu olmalı)
                export SONAR_SCANNER_VERSION="4.7.0.2747" //# <<< BURAYI KENDİ VERSİYONUNUZ İLE DEĞİŞTİRİN!
                export SONAR_SCANNER_ZIP="sonar-scanner-cli-$SONAR_SCANNER_VERSION-linux.zip"
                export SONAR_SCANNER_DOWNLOAD_URL="https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/$SONAR_SCANNER_ZIP"
                // Scanner'ın kurulacağı dizini WORKSPACE içinde belirle
                export SONAR_SCANNER_HOME="$WORKSPACE/.sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux"

                echo "Downloading SonarQube Scanner $SONAR_SCANNER_VERSION..."
                // İndirme (curl veya wget kullanabilirsiniz, agent'ınızda hangisi varsa)
                // --create-dirs: Hedef dizinleri oluşturur
                // -sS: Sessiz mod, hataları gösterir
                // -L: Yönlendirmeleri takip et
                // -o: Çıktıyı dosyaya kaydet
                sh "curl --create-dirs -sSLo $WORKSPACE/.sonar/$SONAR_SCANNER_ZIP $SONAR_SCANNER_DOWNLOAD_URL"

                echo "Extracting SonarQube Scanner..."
                // İndirilen zip dosyasını belirtilen dizine çıkar (-o: üzerine yaz)
                sh "unzip -o $WORKSPACE/.sonar/$SONAR_SCANNER_ZIP -d $WORKSPACE/.sonar/"

                echo "Cleaning up downloaded zip file..."
                // İndirilen zip dosyasını sil
                sh "rm $WORKSPACE/.sonar/$SONAR_SCANNER_ZIP"

                /**# --- ÖNEMLİ: Betik Düzenlemesi ---
                # Eğer önceki sorunları çözmek için betiği manuel düzenlediyseniz (use_embedded_jre=false gibi),
                # bu değişikliği her pipeline çalıştırıldığında otomatik yapmak için sed gibi bir araç kullanabilirsiniz.
                # Ancak, eğer betik içinde JAVA_HOME'u hardcode ettiyseniz ve bu işe yaradıysa,
                # bu sed komutu gerekmeyebilir veya farklı bir sed komutuna ihtiyacınız olabilir.
                # sed -i 's/use_embedded_jre=true/use_embedded_jre=false/g' ${SONAR_SCANNER_HOME}/bin/sonar-scanner # Örnek sed komutu
**/
                echo "SonarQube Scanner PATH environment variable set (for this stage)."
              //  # NOT: Bu PATH ayarı sadece bu 'sh' bloğu için geçerlidir.
               // # Eğer analiz aşaması farklı bir 'sh' bloğu ise, orada tekrar ayarlamak gerekir veya tam yolu kullanmak daha güvenlidir.
                export PATH="${SONAR_SCANNER_HOME}/bin:\$PATH"

                echo "SonarQube Scanner setup complete."
                sh "sonar-scanner --version" //# Kurulumu doğrula

            }
        }

        // --- SonarQube Analiz Aşaması ---
        stage('SonarQube Analysis') {
            steps {
                echo 'Running SonarQube Analysis'
                // Jenkins Credentials Manager'daki token'ı geçici bir ortam değişkeni olarak ayarlar
                // 'sonar-token' -> Credentials Manager'daki Secret Text ID'si (Değiştirin!)
                // 'SONAR_TOKEN' -> Pipeline içinde kullanılacak ortam değişkeni adı
                withCredentials([string(credentialsId: 'sonar-token', variable: 'SONAR_TOKEN')]) {
                    sh '''
                    echo "Starting SonarQube Scanner analysis..."

                    /** # SonarQube Scanner'ın tam yolunu kullanmak en güvenli yoldur,
                    # çünkü PATH ayarının önceki aşamalardan kalıp kalmadığı belirsiz olabilir.
                    # SONAR_SCANNER_HOME değişkeninin hala tanımlı olduğunu varsayıyoruz (Setup aşamasından).
                    # Eğer setup aşaması ayrı bir sh bloğunda ise ve değişken kayboluyorsa,
                    # burada SONAR_SCANNER_HOME'u tekrar belirlemeniz gerekebilir.
                    # export SONAR_SCANNER_VERSION=4.7.0.2747 # <<< BURAYI KENDİ VERSİYONUNUZ İLE DEĞİŞTİRİN!
                    # export SONAR_SCANNER_HOME="$WORKSPACE/.sonar/sonar-scanner-$SONAR_SCANNER_VERSION-linux"


                   /** # SonarQube Scanner komutunu çalıştır
                    # Parametreleri -D ile belirtilir
                    # DİKKAT: Windows için '.bat' değil, Linux shell scripti 'sonar-scanner' kullanıyoruz.
                    # Satır sonlarındaki ters slash ('\\') komutun devam ettiğini belirtir, tek satırda yazarsanız gerekmez. **/
      **/           ${SONAR_SCANNER_HOME}/bin/sonar-scanner \\
                      -D"sonar.projectKey=e-commerce-app" \\    // # <<< BURAYI KENDİ PROJE ANAHTARINIZ İLE DEĞİŞTİRİN!
                      -D"sonar.sources=." \\                  //  # <<< Analiz edilecek dizin (.) mevcut dizin demektir
                      -D"sonar.host.url=http://localhost:9000" // # <<< BURAYI KENDİ SONARQUBE URL'NİZ İLE DEĞİŞTİRİN!
                      -D"sonar.login=$SONAR_TOKEN"             // # <<< TOKEN'I GÜVENLİCE BURADA KULLANIYORUZ!
                      # -D"sonar.python.version=3.x" //# Python projesi için Python versiyonu belirtebilirsiniz

                    echo "SonarQube analysis complete."
                    '''
                }
            }
        }

        // --- İsteğe Bağlı: Quality Gate Kontrol Aşaması ---
        // SonarQube analizinin sonucuna (Quality Gate durumuna) göre pipeline'ın başarılı/başarısız olmasını sağlar.
        // Bunun için SonarQube Scanner plugin'inin kurulu olması gerekir.
        // stage('Quality Gate Check') {
        //     steps {
        //         echo 'Checking Quality Gate status'
        //         // waitForQualityGate adımı SonarQube sunucusundan Quality Gate sonucunu bekler.
        //         // timeout: Belirtilen süre kadar bekler, sonra zaman aşımına uğrar.
        //         // abortPipeline: true -> Quality Gate başarısız olursa pipeline hemen durur.
        //         timeout(time: 10, unit: 'MINUTES') { // <<< Bekleme süresini ayarlayın
        //              waitForQualityGate abortPipeline: true
        //         }
        //         echo 'Quality Gate passed.'
        //     }
        // }
    }
}
