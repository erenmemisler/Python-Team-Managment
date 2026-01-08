import mysql.connector
import hashlib
import secrets
import random
from datetime import datetime, timedelta
from email_utils import validate_email, email_service

try:
    from email_config import configure_email_service
    configure_email_service()
except ImportError:
    pass
except Exception:
    pass


class DatabaseManager:
    def __init__(self):
        # ⚠️ ÖNEMLİ: Veritabanı bilgilerinizi buraya girin
        # ✅ Bu dosya placeholder değerlerle GitHub'a yüklenebilir (güvenli)
        # ⚠️ Kendi bilgilerinizi ekledikten sonra GitHub'a commit etmeyin!
        self.db_config = {
            'host': 'localhost',
            'user': 'root',
            'password': 'your_mysql_password',  # MySQL şifrenizi buraya girin
            'database': 'grup10_startup',
            'port': 3307
        }
        self.connection_error = None
        try:
            self.initialize_database()
        except mysql.connector.Error as e:
            self.connection_error = e
            print(f"⚠️ Veritabanı Bağlantı Hatası: {e}")
            print("💡 MySQL/MAMP'ın çalıştığından ve port 3307'de dinlediğinden emin olun.")

    def get_connection(self):
        if self.connection_error:
            raise self.connection_error
        return mysql.connector.connect(**self.db_config)

    def initialize_database(self):
        try:
            config_no_db = self.db_config.copy()
            config_no_db.pop('database', None)
            conn = mysql.connector.connect(**config_no_db)
            cursor = conn.cursor()
            
            cursor.execute("CREATE DATABASE IF NOT EXISTS grup10_startup")
            conn.commit()
            cursor.close()
            conn.close()
            
            conn = self.get_connection()
            cursor = conn.cursor()
        except mysql.connector.Error as e:
            raise e

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            email VARCHAR(255)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            description TEXT,
            created_by INT,
            status VARCHAR(50) DEFAULT 'Active',
            deadline DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS team_members (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT,
            user_id INT,
            role VARCHAR(50) DEFAULT 'Member',
            joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            sender_id INT,
            receiver_id INT,
            team_id INT,
            message TEXT,
            status VARCHAR(50) DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users(id),
            FOREIGN KEY (receiver_id) REFERENCES users(id),
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INT AUTO_INCREMENT PRIMARY KEY,
            team_id INT,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            assigned_to INT,
            created_by INT,
            status VARCHAR(50) DEFAULT 'Todo',
            deadline DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (team_id) REFERENCES teams(id) ON DELETE CASCADE,
            FOREIGN KEY (assigned_to) REFERENCES users(id),
            FOREIGN KEY (created_by) REFERENCES users(id)
        )
        ''')
        
        try:
            cursor.execute("ALTER TABLE tasks ADD COLUMN created_by INT")
            cursor.execute("ALTER TABLE tasks ADD FOREIGN KEY (created_by) REFERENCES users(id)")
        except:
            pass
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS task_assignments (
            id INT AUTO_INCREMENT PRIMARY KEY,
            task_id INT,
            user_id INT,
            assigned_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (task_id) REFERENCES tasks(id) ON DELETE CASCADE,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE KEY unique_assignment (task_id, user_id)
        )
        ''')

        cursor.execute('''
        CREATE TABLE IF NOT EXISTS password_reset_tokens (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT,
            token VARCHAR(255) UNIQUE NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            INDEX idx_token (token),
            INDEX idx_expires (expires_at)
        )
        ''')

        conn.commit()
        cursor.close()
        conn.close()

    def register_user(self, username, password, email):
        # Email validation
        if email and not validate_email(email):
            return False, "Geçersiz email formatı. Lütfen doğru bir email adresi girin."
        
        conn = self.get_connection()
        cursor = conn.cursor()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        try:
            cursor.execute("INSERT INTO users (username, password_hash, email) VALUES (%s, %s, %s)",
                           (username, hashed_pw, email))
            conn.commit()
            return True, "Kayıt Başarılı!"
        except mysql.connector.IntegrityError:
            return False, "Bu kullanıcı adı zaten alınmış."
        finally:
            cursor.close()
            conn.close()

    def login_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        hashed_pw = hashlib.sha256(password.encode()).hexdigest()
        cursor.execute("SELECT id, username, email FROM users WHERE username=%s AND password_hash=%s",
                       (username, hashed_pw))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return (True, user) if user else (False, None)


    def create_team(self, team_name, description, leader_id, deadline):
        conn = self.get_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO teams (name, description, created_by, deadline) VALUES (%s, %s, %s, %s)",
                           (team_name, description, leader_id, deadline))
            team_id = cursor.lastrowid
            cursor.execute("INSERT INTO team_members (team_id, user_id, role) VALUES (%s, %s, %s)",
                           (team_id, leader_id, 'Leader'))
            conn.commit()
        finally:
            cursor.close()
            conn.close()
        return True, "Proje oluşturuldu!"

    def delete_team(self, team_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE team_id=%s", (team_id,))
        cursor.execute("DELETE FROM notifications WHERE team_id=%s", (team_id,))
        cursor.execute("DELETE FROM team_members WHERE team_id=%s", (team_id,))
        cursor.execute("DELETE FROM teams WHERE id=%s", (team_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def update_team_status(self, team_id, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE teams SET status=%s WHERE id=%s", (status, team_id))
        conn.commit()
        cursor.close()
        conn.close()

    def get_team_details(self, team_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, name, description, created_by, status, deadline FROM teams WHERE id=%s", (team_id,))
        team = cursor.fetchone()
        cursor.close()
        conn.close()
        return team

    def get_user_teams(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT t.id, t.name, t.description, tm.role, t.deadline, t.status
            FROM teams t
            JOIN team_members tm ON t.id = tm.team_id
            WHERE tm.user_id = %s
        '''
        cursor.execute(query, (user_id,))
        teams = cursor.fetchall()
        cursor.close()
        conn.close()
        return teams

    def send_invite(self, sender_id, target_username, team_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Hedef kullanıcıyı bul (id ve email)
        cursor.execute("SELECT id, email FROM users WHERE username=%s", (target_username,))
        target_user = cursor.fetchone()

        if not target_user:
            cursor.close()
            conn.close()
            return False, "Kullanıcı bulunamadı."

        receiver_id = target_user[0]
        receiver_email = target_user[1]
        
        cursor.execute("SELECT * FROM team_members WHERE team_id=%s AND user_id=%s", (team_id, receiver_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return False, "Zaten ekipte."

        cursor.execute("SELECT username FROM users WHERE id=%s", (sender_id,))
        sender_user = cursor.fetchone()
        sender_username = sender_user[0] if sender_user else "Bilinmeyen"

        cursor.execute("SELECT name FROM teams WHERE id=%s", (team_id,))
        team_data = cursor.fetchone()
        team_name = team_data[0] if team_data else "Bilinmeyen Takım"

        msg = "Proje Daveti"
        cursor.execute("INSERT INTO notifications (sender_id, receiver_id, team_id, message) VALUES (%s, %s, %s, %s)",
                       (sender_id, receiver_id, team_id, msg))
        conn.commit()
        
        email_sent = False
        if receiver_email and validate_email(receiver_email):
            try:
                success, email_msg = email_service.send_invite_email(
                    receiver_email, sender_username, team_name, team_id
                )
                if success:
                    email_sent = True
            except Exception as e:
                print(f"Email gönderme hatası (davet kaydedildi): {e}")
        
        cursor.close()
        conn.close()
        
        if email_sent:
            return True, "Davet gönderildi ve email ile bildirildi."
        else:
            return True, "Davet gönderildi. (Email gönderilemedi - email servisi yapılandırılmamış olabilir)"

    def get_my_invites(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT n.id, u.username, t.name, n.message, t.id
            FROM notifications n
            JOIN users u ON n.sender_id = u.id
            JOIN teams t ON n.team_id = t.id
            WHERE n.receiver_id = %s AND n.status = 'Pending'
        '''
        cursor.execute(query, (user_id,))
        invites = cursor.fetchall()
        cursor.close()
        conn.close()
        return invites

    def respond_invite(self, invite_id, accept=True):
        conn = self.get_connection()
        cursor = conn.cursor()
        status = 'Accepted' if accept else 'Rejected'
        cursor.execute("UPDATE notifications SET status=%s WHERE id=%s", (status, invite_id))

        if accept:
            cursor.execute("SELECT receiver_id, team_id FROM notifications WHERE id=%s", (invite_id,))
            data = cursor.fetchone()
            if data:
                cursor.execute("INSERT INTO team_members (team_id, user_id, role) VALUES (%s, %s, %s)",
                               (data[1], data[0], 'Member'))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_team_members(self, team_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        query = '''
            SELECT u.id, u.username, tm.role 
            FROM users u
            JOIN team_members tm ON u.id = tm.user_id
            WHERE tm.team_id = %s
        '''
        cursor.execute(query, (team_id,))
        members = cursor.fetchall()
        cursor.close()
        conn.close()
        return members

    # --- GÖREV İŞLEMLERİ ---
    def create_task(self, team_id, title, description, assigned_to_ids, deadline, created_by_id):
        """
        Görev oluşturur ve birden fazla kişiye atar
        
        Args:
            team_id: Takım ID'si
            title: Görev başlığı
            description: Görev açıklaması
            assigned_to_ids: Atanacak kullanıcı ID'lerinin listesi
            deadline: Son tarih
            created_by_id: Görevi oluşturan kullanıcı ID'si
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # İlk atanan kişiyi eski sisteme uyumluluk için assigned_to'ya kaydet
        primary_assigned = assigned_to_ids[0] if assigned_to_ids else None
        
        cursor.execute('''
            INSERT INTO tasks (team_id, title, description, assigned_to, created_by, deadline, status)
            VALUES (%s, %s, %s, %s, %s, %s, 'Todo')
        ''', (team_id, title, description, primary_assigned, created_by_id, deadline))
        
        task_id = cursor.lastrowid
        
        # Çoklu atamaları task_assignments tablosuna ekle
        if assigned_to_ids:
            for user_id in assigned_to_ids:
                cursor.execute('''
                    INSERT INTO task_assignments (task_id, user_id)
                    VALUES (%s, %s)
                ''', (task_id, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_team_tasks(self, team_id):
        """
        Takım görevlerini getirir (birden fazla atanan kişi ile)
        Returns: [(id, title, description, status, deadline, assigned_names, created_by_id), ...]
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Görevleri getir (created_by dahil)
        query = '''
            SELECT t.id, t.title, t.description, t.status, t.deadline, t.created_by
            FROM tasks t
            WHERE t.team_id = %s
            ORDER BY t.created_at DESC
        '''
        cursor.execute(query, (team_id,))
        tasks = cursor.fetchall()
        
        # Her görev için atanan kişileri getir
        result = []
        for task in tasks:
            task_id = task[0]
            created_by_id = task[5]  # created_by
            # Atanan kişileri getir
            cursor.execute('''
                SELECT u.username
                FROM task_assignments ta
                JOIN users u ON ta.user_id = u.id
                WHERE ta.task_id = %s
            ''', (task_id,))
            assigned_users = cursor.fetchall()
            assigned_names = [user[0] for user in assigned_users] if assigned_users else ["Atanmamış"]
            
            # Görev bilgileri + atanan kişiler + created_by
            result.append((task[0], task[1], task[2], task[3], task[4], assigned_names, created_by_id))
        
        cursor.close()
        conn.close()
        return result

    def mark_task_done(self, task_id, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE tasks SET status='Done' WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def update_task(self, task_id, title, description, assigned_to_ids, deadline, status):
        """
        Görevi günceller ve atamaları yeniler
        
        Args:
            task_id: Görev ID'si
            title: Görev başlığı
            description: Görev açıklaması
            assigned_to_ids: Atanacak kullanıcı ID'lerinin listesi
            deadline: Son tarih
            status: Görev durumu
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # İlk atanan kişiyi eski sisteme uyumluluk için assigned_to'ya kaydet
        primary_assigned = assigned_to_ids[0] if assigned_to_ids else None
        
        cursor.execute('''
            UPDATE tasks 
            SET title=%s, description=%s, assigned_to=%s, deadline=%s, status=%s
            WHERE id=%s
        ''', (title, description, primary_assigned, deadline, status, task_id))
        
        # Eski atamaları sil
        cursor.execute('DELETE FROM task_assignments WHERE task_id=%s', (task_id,))
        
        # Yeni atamaları ekle
        if assigned_to_ids:
            for user_id in assigned_to_ids:
                cursor.execute('''
                    INSERT INTO task_assignments (task_id, user_id)
                    VALUES (%s, %s)
                ''', (task_id, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def delete_task(self, task_id):
        """Görevi siler"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id=%s", (task_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def get_task_by_id(self, task_id):
        """
        ID'ye göre görev bilgilerini getirir (çoklu atama ile)
        Returns: (id, title, description, status, deadline, assigned_user_ids, assigned_user_names, created_by_id, created_by_username, created_at, team_id)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Görev bilgilerini getir (oluşturan kullanıcı bilgisi ile)
        query = '''
            SELECT t.id, t.title, t.description, t.status, t.deadline, t.created_by, t.created_at, t.team_id,
                   u.username as creator_username
            FROM tasks t
            LEFT JOIN users u ON t.created_by = u.id
            WHERE t.id = %s
        '''
        cursor.execute(query, (task_id,))
        task = cursor.fetchone()
        
        if not task:
            cursor.close()
            conn.close()
            return None
        
        # Atanan kullanıcı ID'lerini ve isimlerini getir
        cursor.execute('''
            SELECT ta.user_id, u.username
            FROM task_assignments ta
            JOIN users u ON ta.user_id = u.id
            WHERE ta.task_id = %s
        ''', (task_id,))
        assigned_data = cursor.fetchall()
        assigned_ids = [row[0] for row in assigned_data]
        assigned_names = [row[1] for row in assigned_data]
        
        cursor.close()
        conn.close()
        
        # (id, title, description, status, deadline, assigned_user_ids, assigned_user_names, created_by_id, created_by_username, created_at, team_id)
        return (task[0], task[1], task[2], task[3], task[4], assigned_ids, assigned_names, 
                task[5], task[8], task[6], task[7])

    def request_password_reset(self, email: str) -> tuple[bool, str]:
        """
        Şifre sıfırlama isteği oluşturur ve email gönderir
        
        Args:
            email: Kullanıcının email adresi
            
        Returns:
            tuple: (başarılı mı, mesaj)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Email'e göre kullanıcıyı bul
            cursor.execute("SELECT id, username FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
            
            if not user:
                cursor.close()
                conn.close()
                return False, "Bu email adresi ile kayıtlı kullanıcı bulunamadı."
            
            user_id, username = user
            
            # 6 haneli rakam kodu oluştur
            token = str(random.randint(100000, 999999))
            expires_at = datetime.now() + timedelta(hours=1)  # 1 saat geçerli
            
            # Eski token'ları iptal et
            cursor.execute("UPDATE password_reset_tokens SET used = TRUE WHERE user_id = %s AND used = FALSE", (user_id,))
            
            # Yeni token kaydet
            cursor.execute('''
                INSERT INTO password_reset_tokens (user_id, token, expires_at)
                VALUES (%s, %s, %s)
            ''', (user_id, token, expires_at))
            conn.commit()
            
            cursor.close()
            conn.close()
            
            # Email gönder
            try:
                success, msg = email_service.send_password_reset_email(email, username, token)
                if success:
                    return True, "Şifre sıfırlama kodu email adresinize gönderildi.\n\nLütfen email'inizi kontrol edin ve 6 haneli kodu girin."
                else:
                    return False, f"Email gönderme hatası: {msg}"
            except Exception as e:
                return False, f"Email gönderme hatası: {str(e)}"
        except Exception as e:
            cursor.close()
            conn.close()
            return False, f"Bir hata oluştu: {str(e)}"
    
    def verify_reset_token(self, token: str) -> tuple[bool, int, str]:
        """
        Şifre sıfırlama token'ını doğrular
        
        Args:
            token: Doğrulanacak token
            
        Returns:
            tuple: (geçerli mi, user_id, mesaj)
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                SELECT user_id, expires_at, used
                FROM password_reset_tokens
                WHERE token = %s
            ''', (token,))
            result = cursor.fetchone()
            
            cursor.close()
            conn.close()
            
            if not result:
                return False, None, "Geçersiz token."
            
            user_id, expires_at, used = result
            
            if used:
                return False, None, "Bu token daha önce kullanılmış."
            
            if datetime.now() > expires_at:
                return False, None, "Token'ın süresi dolmuş. Lütfen yeni bir şifre sıfırlama isteği oluşturun."
            
            return True, user_id, "Token geçerli."
        except Exception as e:
            cursor.close()
            conn.close()
            return False, None, f"Hata: {str(e)}"
    
    def reset_password(self, token: str, new_password: str) -> tuple[bool, str]:
        """
        Şifreyi sıfırlar
        
        Args:
            token: Şifre sıfırlama token'ı
            new_password: Yeni şifre
            
        Returns:
            tuple: (başarılı mı, mesaj)
        """
        # Token'ı doğrula
        valid, user_id, msg = self.verify_reset_token(token)
        if not valid:
            return False, msg
        
        # Şifreyi hash'le
        password_hash = hashlib.sha256(new_password.encode()).hexdigest()
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # Şifreyi güncelle
            cursor.execute("UPDATE users SET password_hash = %s WHERE id = %s", (password_hash, user_id))
            
            # Token'ı kullanıldı olarak işaretle
            cursor.execute("UPDATE password_reset_tokens SET used = TRUE WHERE token = %s", (token,))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            return True, "Şifreniz başarıyla güncellendi."
        except Exception as e:
            cursor.close()
            conn.close()
            return False, f"Hata: {str(e)}"