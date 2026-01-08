#!/usr/bin/env python3
"""
Basit Başlatma Scripti - Hataları gösterir
"""

import sys
import traceback

print("=" * 60)
print("🚀 Startup Yönetim Platformu - Başlatılıyor...")
print("=" * 60)
print()

print("📦 Adım 1: Paketler kontrol ediliyor...")
try:
    import customtkinter as ctk
    print("   ✅ customtkinter yüklü")
except ImportError as e:
    print(f"   ❌ customtkinter yüklü değil: {e}")
    print("   💡 Çözüm: pip3 install customtkinter")
    sys.exit(1)

try:
    import mysql.connector
    print("   ✅ mysql-connector-python yüklü")
except ImportError as e:
    print(f"   ❌ mysql-connector-python yüklü değil: {e}")
    print("   💡 Çözüm: pip3 install mysql-connector-python")
    sys.exit(1)

print("\n📊 Adım 2: Veritabanı bağlantısı test ediliyor...")
try:
    from db_manager import DatabaseManager
    db = DatabaseManager()
    if db.connection_error:
        print(f"   ❌ Veritabanı bağlantı hatası: {db.connection_error}")
        print("\n   💡 Çözüm adımları:")
        print("   1. MAMP'ı açın ve 'Start Servers' butonuna tıklayın")
        print("   2. MySQL'in yeşil ışık yaktığını kontrol edin")
        print("   3. Port 3307'nin açık olduğunu kontrol edin")
        print("   4. db_manager.py dosyasındaki şifreyi kontrol edin")
        sys.exit(1)
    else:
        print("   ✅ Veritabanı bağlantısı başarılı")
except Exception as e:
    print(f"   ❌ Veritabanı hatası: {e}")
    traceback.print_exc()
    sys.exit(1)

print("\n🖥️  Adım 3: GUI başlatılıyor...")
try:
    from Grup10_Proje import MainApp
    print("   ✅ MainApp import edildi")
    
    print("\n" + "=" * 60)
    print("✅ Tüm kontroller başarılı! Uygulama açılıyor...")
    print("=" * 60)
    print()
    
    app = MainApp()
    app.mainloop()
    
except KeyboardInterrupt:
    print("\n\n⚠️  Uygulama kullanıcı tarafından kapatıldı.")
except Exception as e:
    print(f"\n❌ Uygulama başlatılamadı: {e}")
    print("\n📋 Detaylı hata bilgisi:")
    traceback.print_exc()
    print("\n" + "=" * 60)
    input("Devam etmek için Enter'a basın...")
    sys.exit(1)


