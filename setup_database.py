#!/usr/bin/env python3
"""
MySQL Veritabanı Kurulum Scripti
Bu script MySQL bağlantısını test eder ve veritabanını oluşturur.
"""

import mysql.connector
from mysql.connector import Error

def test_connection():
    """
    MySQL bağlantısını test eder
    
    ⚠️ NOT: Bu script yaygın varsayılan şifreleri test eder.
    Bu sadece yerel geliştirme ortamları için kullanılmalıdır.
    Production ortamında asla kullanmayın!
    """
    configs = [
        # MAMP için varsayılan ayarlar (yerel geliştirme için)
        {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',  # ⚠️ MAMP varsayılan şifresi - kendi şifrenizi kullanın
            'port': 3307
        },
        # Standart MySQL ayarları (yerel geliştirme için)
        {
            'host': 'localhost',
            'user': 'root',
            'password': '',  # ⚠️ Boş şifre - kendi şifrenizi kullanın
            'port': 3306
        },
        {
            'host': 'localhost',
            'user': 'root',
            'password': 'root',  # ⚠️ Varsayılan şifre - kendi şifrenizi kullanın
            'port': 3306
        }
    ]
    
    print("🔍 MySQL bağlantısı test ediliyor...\n")
    
    for i, config in enumerate(configs, 1):
        try:
            print(f"Deneme {i}: {config['host']}:{config['port']} - Kullanıcı: {config['user']}")
            conn = mysql.connector.connect(**config)
            print(f"✅ Bağlantı başarılı! Port: {config['port']}\n")
            conn.close()
            return config
        except Error as e:
            print(f"❌ Bağlantı başarısız: {e}\n")
    
    return None

def create_database(config):
    """Veritabanını oluşturur"""
    try:
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()
        
        # Veritabanını oluştur
        cursor.execute("CREATE DATABASE IF NOT EXISTS grup10_startup")
        print("✅ Veritabanı 'grup10_startup' oluşturuldu/kontrol edildi.")
        
        cursor.close()
        conn.close()
        return True
    except Error as e:
        print(f"❌ Veritabanı oluşturulamadı: {e}")
        return False

def main():
    print("=" * 50)
    print("MySQL Veritabanı Kurulum Aracı")
    print("=" * 50)
    print()
    
    # Bağlantıyı test et
    config = test_connection()
    
    if not config:
        print("\n❌ MySQL bağlantısı kurulamadı!")
        print("\n💡 Yapılacaklar:")
        print("1. MAMP/MySQL'in çalıştığından emin olun")
        print("2. MAMP'ta MySQL'in başlatıldığını kontrol edin")
        print("3. Port numarasını kontrol edin (MAMP genelde 3307, standart MySQL 3306)")
        print("4. Kullanıcı adı ve şifreyi kontrol edin")
        return
    
    # Veritabanını oluştur
    print("📦 Veritabanı oluşturuluyor...")
    if create_database(config):
        print("\n✅ Kurulum tamamlandı!")
        print(f"\n📝 db_manager.py dosyasında şu ayarları kullanın:")
        print(f"   host: '{config['host']}'")
        print(f"   port: {config['port']}")
        print(f"   user: '{config['user']}'")
        print(f"   password: '{config['password']}'")
    else:
        print("\n❌ Kurulum başarısız!")

if __name__ == "__main__":
    main()


