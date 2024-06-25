# Kişiselleştirilmiş Bildirimler Projesi

## Proje Genel Bakış
Kişiselleştirilmiş Bildirimler Projesi'ne hoş geldiniz! Bu yenilikçi çözüm, müşteri verilerini gerçek zamanlı olarak kullanarak ilgilerine ve davranışlarına göre kişiselleştirilmiş bildirimler sunar. Projemizin amacı, Fibabanka'nın dijital bankacılık ekosistemini geliştirerek müşteri etkileşimini artırmak, kullanıcı deneyimini iyileştirmek ve bildirim stratejilerini optimize etmektir.

## Temel Özellikler
Gerçek Zamanlı Veri İşleme: Kafka ve Spark kullanarak kesintisiz veri alımı ve işleme.
Kategori Analizi: Müşteri davranışlarını analiz ederek ilgi duydukları ana kategorileri belirleme.
Kişiselleştirilmiş Bildirimler: Müşteri ilgilerine göre hedeflenmiş bildirimler gönderme.
Deep Reinforcement Learning: Gelecekte bildirim stratejilerini optimize etmek için DRL modellerinin uygulanması.
Ölçeklenebilir Mimari: Fibabanka'nın mevcut altyapısıyla entegre olacak şekilde tasarlandı.
Test için Mock Veri: Gerçek dünya senaryolarını simüle etmek için mock veri scriptleri.

## Teknik Detaylar
### Veri İşleme
Spark ve Starburst kullanarak Countly tablolarından gerçek zamanlı müşteri verilerini işliyoruz. Scriptlerimiz, müşteri ilgilerini belirlemek için verilerin verimli bir şekilde alınmasını ve dönüştürülmesini sağlar.
### Kategori Analizi
Müşteri etkileşimlerini analiz ederek en çok ilgilendikleri kategorileri belirliyoruz. Bu bilgi, ilgili bildirimler göndermek için kritik öneme sahiptir.

### Bildirim Gönderimi
Müşteri ilgilerine dayalı kişiselleştirilmiş bildirimler gönderilir. Bu, verimli veri hatları ve gerçek zamanlı işleme kullanılarak gerçekleştirilir.

### Deep Reinforcement Learning
Gelecek yol haritamızda, bildirim stratejilerini optimize etmek için Deep Reinforcement Learning (DRL) modelleri uygulamayı planlıyoruz. Bu modeller, müşteri yanıtlarını dikkate alacak ve etkileşimi en üst düzeye çıkarmak için uyum sağlayacaktır.

## Gelecek Potansiyeli
Deep Reinforcement Learning: Müşteri yanıtlarından öğrenerek bildirim stratejilerini optimize etme.
Geliştirilmiş Kullanıcı Deneyimi: Müşteri etkileşimlerine dayalı olarak uygulama deneyimini kişiselleştirme.
Artan Etkileşim: İlgili bildirimler aracılığıyla uygulama kullanımını ve müşteri memnuniyetini artırma.

## Çalıştırma Adımları
### Gereksinimler
Python 3.8 veya üstü
Spark
Kafka
Starburst
Airflow
Gerekli Python paketleri (bkz. requirements.txt)

### Adımlar
#### 1. Repository'i klonlayın:
git clone https://github.com/KutluhanI/Hackathon/
cd personalized_notifications
#### 2. Gerekli paketleri yükleyin:
pip install -r personalized_notifications/requirements.txt
#### 3. Veri işleme scriptini çalıştırın:
python personalized_notifications/scripts/data_processing.py
#### 4. Kategori analizi scriptini çalıştırın:
python personalized_notifications/scripts/category_analysis.py
#### 5. Bildirimleri gönderin:
python personalized_notifications/scripts/notification_sender.py
#### 6. Deep Reinforcement Learning modelini çalıştırın:
python personalized_notifications/scripts/drl_model.py

## Sonuç
Kişiselleştirilmiş Bildirimler Projesi, Fibabanka'nın mobil uygulamasını son derece kişiselleştirilmiş ve etkileşimli bir deneyime dönüştürmek için tasarlanmıştır. İleri düzey veri işleme ve makine öğrenimi tekniklerinden yararlanarak, ilgili bildirimler sunabilir, müşteri memnuniyetini artırabilir ve uygulama kullanımını teşvik edebiliriz. Bu proje, mevcut ihtiyaçları karşılamakla kalmaz, aynı zamanda Deep Reinforcement Learning ile gelecekteki yenilikler için de temel oluşturur.
