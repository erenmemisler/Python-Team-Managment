# Startup Yönetim Platformu

Modern bir GUI tabanlı startup ve proje yönetim platformu. Takımlar oluşturun, görevler atayın ve projelerinizi organize edin.

## 🚀 Özellikler

- **Kullanıcı Yönetimi**: Kayıt, giriş ve şifre sıfırlama
- **Takım Yönetimi**: Takımlar oluşturma, düzenleme ve silme
- **Görev Yönetimi**: Görevler oluşturma, atama ve takip
- **Davet Sistemi**: Takım üyelerine davet gönderme
- **Email Bildirimleri**: Takım davetleri ve şifre sıfırlama email'leri
- **Modern GUI**: CustomTkinter ile modern ve kullanıcı dostu arayüz

## 📋 Gereksinimler

- Python 3.8 veya üzeri
- MySQL/MAMP (veritabanı için)
- Python paketleri (requirements.txt'de listelenmiştir)

## 🔧 Kurulum

### 1. Depoyu Klonlayın

```bash
git clone <repository-url>
cd "20242425038_BatuhanSancak_ErenMemisler_20232425062/Python Proje"
```

### 2. Python Paketlerini Yükleyin

```bash
pip3 install -r requirements.txt
```

### 3. Veritabanını Yapılandırın

1. **MAMP'ı başlatın** ve MySQL servisinin çalıştığından emin olun
2. MySQL port'unun **3307** olduğundan emin olun (MAMP varsayılan portu)

### 4. Yapılandırma Dosyalarını Düzenleyin

⚠️ **ÖNEMLİ**: Uygulamayı kullanmadan önce aşağıdaki dosyaları düzenleyip kendi bilgilerinizi girin:

#### a) Veritabanı Ayarları (`db_manager.py`)

`db_manager.py` dosyasını açın ve `DatabaseManager` sınıfındaki `__init__` metodunda:

```python
self.db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_mysql_password',  # ← MySQL şifrenizi buraya girin
    'database': 'grup10_startup',
    'port': 3307
}
```

#### b) Email Ayarları (`email_config.py`)

`email_config.py` dosyasını açın ve `EMAIL_CONFIG` dictionary'sini düzenleyin:

```python
EMAIL_CONFIG = {
    'sender_email': 'your-email@gmail.com',  # ← Email adresinizi buraya girin
    'sender_password': 'your_app_password',  # ← Gmail App Password'unuzu buraya girin
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}
```

**Önemli**: Gmail kullanıyorsanız, normal şifre yerine **App Password** kullanmanız gerekmektedir:

- Google Account > Security > 2-Step Verification > App Passwords
- Yeni bir App Password oluşturun ve `email_config.py` dosyasına ekleyin

### 5. Veritabanını Oluşturun

Uygulama ilk çalıştırıldığında veritabanı ve tablolar otomatik olarak oluşturulacaktır.

## 🎮 Kullanım

Uygulamayı başlatmak için:

```bash
python3 baslat.py
```

veya doğrudan:

```bash
python3 Grup10_Proje.py
```

## 📁 Proje Yapısı

```
Python Proje/
├── baslat.py              # Başlatma scripti (hata kontrolü ile)
├── Grup10_Proje.py        # Ana uygulama dosyası
├── db_manager.py          # Veritabanı yönetim sınıfı (yapılandırma gerekli)
├── email_config.py        # Email servisi yapılandırması (yapılandırma gerekli)
├── email_utils.py         # Email utility fonksiyonları
├── setup_database.py      # Veritabanı kurulum scripti
├── test_connection.py     # Bağlantı test scripti
├── requirements.txt       # Python bağımlılıkları
└── README.md              # Bu dosya
```

## 🔒 Güvenlik

- **✅ Proje GitHub'a yüklemek için hazırdır** - Tüm hassas bilgiler placeholder değerlerle saklanmıştır
- **Hassas bilgiler kod içinde placeholder olarak saklanır** - `db_manager.py` ve `email_config.py` dosyalarında kendi bilgilerinizi girmeniz gerekir
- **⚠️ ÖNEMLİ**: Kendi bilgilerinizi ekledikten sonra GitHub'a commit etmeyin! Placeholder değerlere geri döndürün
- Şifreler SHA-256 ile hash'lenir
- Email şifreleri App Password kullanır (Gmail için)
- `setup_database.py` dosyası yaygın varsayılan şifreleri test eder (sadece yerel geliştirme için)

## 🛠️ Geliştirme

### Veritabanı Şeması

Uygulama aşağıdaki tabloları kullanır:

- `users` - Kullanıcı bilgileri
- `teams` - Takım/Proje bilgileri
- `team_members` - Takım üyelikleri
- `tasks` - Görevler
- `task_assignments` - Görev atamaları (çoklu atama desteği)
- `notifications` - Bildirimler ve davetler
- `password_reset_tokens` - Şifre sıfırlama token'ları

## 📝 Lisans

Bu proje eğitim amaçlı geliştirilmiştir.

## 👥 Yazarlar

- Batuhan Sancak (20242425038)
- Eren Memişler (20232425062)

## ⚠️ Sorun Giderme

### MySQL Bağlantı Hatası

- MAMP'ın çalıştığından emin olun
- MySQL port'unun 3307 olduğunu kontrol edin
- `db_manager.py` dosyasındaki veritabanı bilgilerini kontrol edin
- `password` değerinin `'your_mysql_password'` yerine gerçek şifreniz olduğundan emin olun

### Email Gönderme Hatası

- Gmail kullanıyorsanız App Password kullandığınızdan emin olun
- `email_config.py` dosyasındaki email ayarlarını kontrol edin
- `sender_email` ve `sender_password` değerlerinin placeholder değil gerçek değerler olduğundan emin olun
- SMTP port'unun doğru olduğunu kontrol edin (587)

### Paket Yükleme Hatası

```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

## 📞 İletişim

Sorularınız için issue açabilirsiniz.
