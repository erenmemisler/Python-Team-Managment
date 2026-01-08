"""
Email Utility Fonksiyonları
- Email validation
- Email gönderme servisi
"""

import re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional


def validate_email(email: str) -> bool:
    """
    Email formatını kontrol eder
    
    Args:
        email: Kontrol edilecek email adresi
        
    Returns:
        bool: Email geçerliyse True, değilse False
    """
    if not email or not isinstance(email, str):
        return False
    
    # Basit email regex pattern
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email.strip()))


class EmailService:
    """Email gönderme servisi"""
    
    def __init__(self):
        # Varsayılan değerler - email_config.py'den configure() ile ayarlanmalı
        self.smtp_server = 'smtp.gmail.com'
        self.smtp_port = 587
        self.sender_email = ''  # email_config.py'den configure() ile ayarlanmalı
        self.sender_password = ''  # email_config.py'den configure() ile ayarlanmalı
        
    def configure(self, sender_email: str, sender_password: str, 
                  smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Email servisini yapılandırır
        
        Args:
            sender_email: Gönderen email adresi
            sender_password: Gönderen email şifresi (veya app password)
            smtp_server: SMTP sunucu adresi
            smtp_port: SMTP port numarası
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
    
    def send_invite_email(self, receiver_email: str, sender_username: str, 
                         team_name: str, team_id: int) -> tuple[bool, str]:
        """
        Takım daveti email'i gönderir
        
        Args:
            receiver_email: Alıcı email adresi
            sender_username: Gönderen kullanıcı adı
            team_name: Takım adı
            team_id: Takım ID'si
            
        Returns:
            tuple: (başarılı mı, mesaj)
        """
        if not self.sender_email or not self.sender_password:
            return False, "Email servisi yapılandırılmamış. Lütfen SMTP ayarlarını yapın."
        
        if not validate_email(receiver_email):
            return False, "Geçersiz email adresi"
        
        try:
            subject = f"🎯 {team_name} Takımına Davet Aldınız!"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4CAF50;">Takım Daveti</h2>
                    <p>Merhaba,</p>
                    <p><strong>{sender_username}</strong> sizi <strong>{team_name}</strong> takımına katılmaya davet ediyor!</p>
                    <div style="background-color: #f4f4f4; padding: 15px; border-radius: 5px; margin: 20px 0;">
                        <p style="margin: 0;"><strong>Takım:</strong> {team_name}</p>
                        <p style="margin: 5px 0;"><strong>Davet Eden:</strong> {sender_username}</p>
                    </div>
                    <p>Uygulamaya giriş yaparak daveti kabul edebilirsiniz.</p>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Takım Daveti
            
            Merhaba,
            
            {sender_username} sizi {team_name} takımına katılmaya davet ediyor!
            
            Takım: {team_name}
            Davet Eden: {sender_username}
            
            Uygulamaya giriş yaparak daveti kabul edebilirsiniz.
            
            ---
            Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = receiver_email
            
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            
            message.attach(part1)
            message.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True, "Email başarıyla gönderildi"
            
        except smtplib.SMTPAuthenticationError:
            return False, "Email kimlik doğrulama hatası. Lütfen email ve şifrenizi kontrol edin."
        except smtplib.SMTPException as e:
            return False, f"Email gönderme hatası: {str(e)}"
        except Exception as e:
            return False, f"Beklenmeyen hata: {str(e)}"
    
    def send_welcome_email(self, receiver_email: str, username: str) -> tuple[bool, str]:
        """
        Hoş geldin email'i gönderir
        
        Args:
            receiver_email: Alıcı email adresi
            username: Kullanıcı adı
            
        Returns:
            tuple: (başarılı mı, mesaj)
        """
        if not self.sender_email or not self.sender_password:
            return False, "Email servisi yapılandırılmamış"
        
        if not validate_email(receiver_email):
            return False, "Geçersiz email adresi"
        
        try:
            subject = "🎉 Startup Yönetim Platformu'na Hoş Geldiniz!"
            
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4CAF50;">Hoş Geldiniz!</h2>
                    <p>Merhaba <strong>{username}</strong>,</p>
                    <p>Startup Yönetim Platformu'na başarıyla kaydoldunuz!</p>
                    <p>Artık takımlar oluşturabilir, görevler yönetebilir ve projelerinizi organize edebilirsiniz.</p>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Hoş Geldiniz!
            
            Merhaba {username},
            
            Startup Yönetim Platformu'na başarıyla kaydoldunuz!
            
            Artık takımlar oluşturabilir, görevler yönetebilir ve projelerinizi organize edebilirsiniz.
            
            ---
            Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = receiver_email
            
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            
            message.attach(part1)
            message.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True, "Hoş geldin email'i gönderildi"
            
        except Exception as e:
            return False, f"Email gönderme hatası: {str(e)}"
    
    def send_password_reset_email(self, receiver_email: str, username: str, 
                                  token: str) -> tuple[bool, str]:
        """
        Şifre sıfırlama email'i gönderir
        
        Args:
            receiver_email: Alıcı email adresi
            username: Kullanıcı adı
            token: Şifre sıfırlama token'ı
            
        Returns:
            tuple: (başarılı mı, mesaj)
        """
        if not self.sender_email or not self.sender_password:
            return False, "Email servisi yapılandırılmamış. Lütfen SMTP ayarlarını yapın."
        
        if not validate_email(receiver_email):
            return False, "Geçersiz email adresi"
        
        try:
            subject = "🔐 Şifre Sıfırlama İsteği"
            
            # Token'ı email içinde gönder (gerçek uygulamada link olmalı)
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    <h2 style="color: #4CAF50;">Şifre Sıfırlama</h2>
                    <p>Merhaba <strong>{username}</strong>,</p>
                    <p>Şifre sıfırlama isteğiniz alındı. Aşağıdaki kodu kullanarak şifrenizi sıfırlayabilirsiniz.</p>
                    <div style="background-color: #f4f4f4; padding: 25px; border-radius: 8px; margin: 20px 0; text-align: center; border: 2px dashed #4CAF50;">
                        <p style="margin: 0; font-size: 36px; font-weight: bold; color: #4CAF50; letter-spacing: 8px; font-family: 'Courier New', monospace;">{token}</p>
                    </div>
                    <p style="text-align: center; color: #666; font-size: 13px;">Bu kodu şifre sıfırlama ekranına girin</p>
                    <p style="color: #ff9800; font-weight: bold;">⚠️ Bu kod 1 saat geçerlidir.</p>
                    <p style="color: #666; font-size: 12px; margin-top: 30px;">
                        Eğer bu isteği siz yapmadıysanız, bu email'i görmezden gelebilirsiniz.
                    </p>
                    <p style="color: #666; font-size: 12px;">
                        Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
                    </p>
                </div>
            </body>
            </html>
            """
            
            text_body = f"""
            Şifre Sıfırlama
            
            Merhaba {username},
            
            Şifre sıfırlama isteğiniz alındı. Aşağıdaki kodu kullanarak şifrenizi sıfırlayabilirsiniz.
            
            Kod: {token}
            
            ⚠️ Bu kod 1 saat geçerlidir.
            
            Eğer bu isteği siz yapmadıysanız, bu email'i görmezden gelebilirsiniz.
            
            ---
            Bu email Startup Yönetim Platformu tarafından gönderilmiştir.
            """
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.sender_email
            message["To"] = receiver_email
            
            part1 = MIMEText(text_body, "plain")
            part2 = MIMEText(html_body, "html")
            
            message.attach(part1)
            message.attach(part2)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(message)
            
            return True, "Şifre sıfırlama email'i gönderildi"
            
        except Exception as e:
            return False, f"Email gönderme hatası: {str(e)}"


# Global email service instance
email_service = EmailService()

