"""
Email Servisi Yapılandırma Dosyası

⚠️ ÖNEMLİ: Email bilgilerinizi buraya girin
✅ Bu dosya placeholder değerlerle GitHub'a yüklenebilir (güvenli)
⚠️ Kendi bilgilerinizi ekledikten sonra GitHub'a commit etmeyin!

Gmail kullanıyorsanız, normal şifre yerine "App Password" kullanmanız gerekmektedir:
Google Account > Security > 2-Step Verification > App Passwords
"""

from email_utils import email_service

# ⚠️ ÖNEMLİ: Kendi email bilgilerinizi buraya girin
EMAIL_CONFIG = {
    'sender_email': 'your-email@gmail.com',  # Email adresinizi buraya girin
    'sender_password': 'your_app_password',  # Gmail App Password'unuzu buraya girin
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587
}


def configure_email_service():
    """
    Email servisini yapılandırır
    Bu fonksiyon uygulama başlatılırken çağrılmalı
    """
    if EMAIL_CONFIG['sender_email'] and EMAIL_CONFIG['sender_email'] != 'your-email@gmail.com':
        email_service.configure(
            sender_email=EMAIL_CONFIG['sender_email'],
            sender_password=EMAIL_CONFIG['sender_password'],
            smtp_server=EMAIL_CONFIG['smtp_server'],
            smtp_port=EMAIL_CONFIG['smtp_port']
        )
        return True
    return False

