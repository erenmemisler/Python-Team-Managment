#!/usr/bin/env python3
"""Hızlı bağlantı testi"""

import sys
try:
    from db_manager import DatabaseManager
    print("✅ db_manager import edildi")
except Exception as e:
    print(f"❌ Import hatası: {e}")
    sys.exit(1)

try:
    db = DatabaseManager()
    if db.connection_error:
        print(f"❌ Bağlantı hatası: {db.connection_error}")
        print("\n🔧 Çözüm önerileri:")
        print("1. MAMP'ı başlatın ve MySQL'i çalıştırın")
        print("2. Port 3307'yi kontrol edin")
        print("3. Şifreyi kontrol edin (db_manager.py satır 12)")
        sys.exit(1)
    else:
        print("✅ Veritabanı bağlantısı başarılı!")
        print("✅ Proje çalışmaya hazır!")
except Exception as e:
    print(f"❌ Beklenmeyen hata: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)


