import customtkinter as ctk
from tkinter import messagebox
from db_manager import DatabaseManager
from email_utils import validate_email

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

COLORS = {
    'bg_primary': '#1a1a1a',
    'bg_secondary': '#2b2b2b',
    'bg_tertiary': '#3a3a3a',
    'accent_primary': '#4a9eff',
    'accent_secondary': '#5cb85c',
    'accent_danger': '#d9534f',
    'text_primary': '#ffffff',
    'text_secondary': '#b0b0b0',
    'text_muted': '#808080',
    'border': '#404040',
    'hover': '#353535'
}


class MainApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Startup Yönetim Platformu")
        self.geometry("1200x800")
        self.minsize(1000, 700)

        try:
            self.db = DatabaseManager()
            if self.db.connection_error:
                messagebox.showerror(
                    "Veritabanı Hatası",
                    f"MySQL bağlantısı kurulamadı!\n\n"
                    f"Hata: {self.db.connection_error}\n\n"
                    f"Lütfen kontrol edin:\n"
                    f"1. MySQL/MAMP çalışıyor mu?\n"
                    f"2. Port 3307 doğru mu?\n"
                    f"3. Veritabanı 'grup10_startup' oluşturuldu mu?\n"
                    f"4. Kullanıcı adı/şifre doğru mu?"
                )
                self.destroy()
                return
        except Exception as e:
            messagebox.showerror("Başlatma Hatası",
                                 f"Uygulama başlatılamadı.\n\nHata detayı: {e}\n\nLütfen sistem yöneticinize başvurun.")
            self.destroy()
            return

        self.show_login_frame()

    def show_login_frame(self):
        """Giriş Ekranı - Modern Split Design (Batuhan Sancak & Eren Memişler)"""
        for widget in self.winfo_children():
            widget.destroy()

        main_bg = ctk.CTkFrame(self, fg_color=COLORS['bg_primary'])
        main_bg.pack(fill="both", expand=True)

        main_container = ctk.CTkFrame(main_bg, fg_color="transparent")
        main_container.pack(expand=True, fill="both", padx=50, pady=50)

        content_box = ctk.CTkFrame(main_container, fg_color=COLORS['bg_secondary'], corner_radius=30, border_width=0)
        content_box.pack(expand=True, fill="both")

        info_frame = ctk.CTkFrame(content_box, fg_color=COLORS['accent_primary'], corner_radius=30)
        info_frame.pack(side="left", fill="both", expand=True, padx=(0, 0))

        info_content = ctk.CTkFrame(info_frame, fg_color="transparent")
        info_content.pack(expand=True, fill="x", padx=50)

        ctk.CTkLabel(info_content, text="🚀",
                     font=("SF Pro Display", 64)).pack(anchor="w", pady=(0, 10))

        ctk.CTkLabel(info_content, text="STARTUP\nYÖNETİM\nPLATFORMU",
                     font=("SF Pro Display", 42, "bold"),
                     text_color="#ffffff",
                     justify="left",
                     height=120).pack(anchor="w", pady=(0, 15))

        description_text = (
            "Kaosu düzene dönüştürün.\n"
            "Yazılım ekipleri için tasarlanmış yeni nesil görev ve proje yönetim aracı."
        )
        ctk.CTkLabel(info_content, text=description_text,
                     font=("SF Pro Display", 16),
                     text_color="#e6f2ff",
                     wraplength=350,
                     justify="left").pack(anchor="w", pady=(0, 35))

        features_frame = ctk.CTkFrame(info_content, fg_color="transparent")
        features_frame.pack(anchor="w", pady=(0, 40))

        feature_list = [
            ("👥", "Çevik Takım Yönetimi"),
            ("📋", "Kanban Tarzı Görev Takibi"),
            ("🔐", "Rol Tabanlı Güvenlik"),
            ("📊", "Anlık Proje Genel Bakışı")
        ]

        for icon, text in feature_list:
            row = ctk.CTkFrame(features_frame, fg_color="transparent")
            row.pack(fill="x", pady=5)
            ctk.CTkLabel(row, text=icon, font=("SF Pro Display", 18), text_color="#ffffff").pack(side="left",
                                                                                                 padx=(0, 10))
            ctk.CTkLabel(row, text=text, font=("SF Pro Display", 15, "bold"), text_color="#ffffff").pack(side="left")

        dev_frame = ctk.CTkFrame(info_content, fg_color="transparent")
        dev_frame.pack(anchor="w", side="bottom", pady=(20, 0))
        ctk.CTkLabel(dev_frame, text="🛠️ Geliştiriciler",
                     font=("SF Pro Display", 12, "bold"), text_color="#cce5ff").pack(anchor="w")
        ctk.CTkLabel(dev_frame, text="Batuhan Sancak ve Eren Memişler",
                     font=("SF Pro Display", 14),
                     text_color="#ffffff").pack(anchor="w")

        login_frame = ctk.CTkFrame(content_box, fg_color="transparent")
        login_frame.pack(side="right", fill="both", expand=True)

        form_center = ctk.CTkFrame(login_frame, fg_color="transparent")
        form_center.pack(expand=True, padx=40)

        ctk.CTkLabel(form_center, text="Tekrar Hoş Geldiniz",
                     font=("SF Pro Display", 32, "bold"),
                     text_color=COLORS['text_primary']).pack(pady=(0, 10))

        ctk.CTkLabel(form_center, text="Devam etmek için giriş yapın",
                     font=("SF Pro Display", 15),
                     text_color=COLORS['text_secondary']).pack(pady=(0, 40))

        entry_width = 320
        entry_height = 50

        ctk.CTkLabel(form_center, text="Kullanıcı Adı", font=("SF Pro Display", 13, "bold"),
                     text_color=COLORS['text_secondary'], anchor="w").pack(fill="x", pady=(0, 8))
        self.entry_user = ctk.CTkEntry(form_center, placeholder_text="Kullanıcı adınızı girin", width=entry_width,
                                       height=entry_height, corner_radius=12, border_width=1,
                                       border_color=COLORS['border'], font=("SF Pro Display", 15))
        self.entry_user.pack(pady=(0, 20))

        ctk.CTkLabel(form_center, text="Şifre", font=("SF Pro Display", 13, "bold"),
                     text_color=COLORS['text_secondary'], anchor="w").pack(fill="x", pady=(0, 8))
        self.entry_pass = ctk.CTkEntry(form_center, placeholder_text="••••••••", show="*", width=entry_width,
                                       height=entry_height, corner_radius=12, border_width=1,
                                       border_color=COLORS['border'], font=("SF Pro Display", 15))
        self.entry_pass.pack(pady=(0, 10))

        link_forgot = ctk.CTkButton(form_center, text="Şifremi Unuttum?", fg_color="transparent",
                                    hover_color=COLORS['hover'], text_color=COLORS['accent_primary'],
                                    font=("SF Pro Display", 13), command=self.show_forgot_password_dialog, height=25,
                                    anchor="e")
        link_forgot.pack(fill="x", pady=(0, 30))

        btn_login = ctk.CTkButton(form_center, text="🚀 Giriş Yap", command=self.handle_login, width=entry_width,
                                  height=55, corner_radius=12, fg_color=COLORS['accent_primary'], hover_color="#3a8eef",
                                  font=("SF Pro Display", 16, "bold"))
        btn_login.pack(pady=(0, 20))

        register_frame = ctk.CTkFrame(form_center, fg_color="transparent")
        register_frame.pack()
        ctk.CTkLabel(register_frame, text="Hesabınız yok mu?", font=("SF Pro Display", 14),
                     text_color=COLORS['text_secondary']).pack(side="left")
        link_register = ctk.CTkButton(register_frame, text="Hemen Kayıt Olun", fg_color="transparent",
                                      hover_color=COLORS['hover'], text_color=COLORS['accent_primary'],
                                      font=("SF Pro Display", 14, "bold"), command=self.show_register_frame, height=30,
                                      width=120)
        link_register.pack(side="left", padx=(5, 0))

    def show_register_frame(self):
        """Kayıt Ol Ekranını Çizer"""
        for widget in self.winfo_children():
            widget.destroy()

        main_container = ctk.CTkFrame(self, fg_color="transparent")
        main_container.pack(fill="both", expand=True, padx=50, pady=30)

        frame = ctk.CTkFrame(main_container, width=420, height=620,
                            corner_radius=24, fg_color=COLORS['bg_secondary'],
                            border_width=0)
        frame.pack(expand=True)
        frame.pack_propagate(False)

        header_frame = ctk.CTkFrame(frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=40, pady=(40, 20))

        title_label = ctk.CTkLabel(header_frame, text="Hesap Oluştur",
                                  font=("SF Pro Display", 32, "bold"),
                                  text_color=COLORS['text_primary'])
        title_label.pack()

        subtitle_label = ctk.CTkLabel(header_frame, text="Yeni bir hesap oluşturun",
                                     font=("SF Pro Display", 14),
                                     text_color=COLORS['text_secondary'])
        subtitle_label.pack(pady=(5, 0))

        form_frame = ctk.CTkScrollableFrame(frame, fg_color="transparent")
        form_frame.pack(fill="both", expand=True, padx=40, pady=20)

        ctk.CTkLabel(form_frame, text="Kullanıcı Adı",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        self.reg_user = ctk.CTkEntry(form_frame, placeholder_text="Kullanıcı adınızı girin",
                                    width=340, height=48,
                                    corner_radius=12, border_width=1,
                                    border_color=COLORS['border'],
                                    font=("SF Pro Display", 14))
        self.reg_user.pack(pady=(0, 16))

        ctk.CTkLabel(form_frame, text="E-Posta",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        self.reg_email = ctk.CTkEntry(form_frame, placeholder_text="E-posta adresinizi girin",
                                     width=340, height=48,
                                     corner_radius=12, border_width=1,
                                     border_color=COLORS['border'],
                                     font=("SF Pro Display", 14))
        self.reg_email.pack(pady=(0, 16))

        ctk.CTkLabel(form_frame, text="Şifre",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        self.reg_pass = ctk.CTkEntry(form_frame, placeholder_text="Şifrenizi oluşturun",
                                    show="*", width=340, height=48,
                                    corner_radius=12, border_width=1,
                                    border_color=COLORS['border'],
                                    font=("SF Pro Display", 14))
        self.reg_pass.pack(pady=(0, 16))

        ctk.CTkLabel(form_frame, text="Rol",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        self.reg_role = ctk.CTkComboBox(form_frame,
                                       values=["Team Leader", "Coder", "Designer", "Marketing"],
                                       width=340, height=48,
                                       corner_radius=12, border_width=1,
                                       border_color=COLORS['border'],
                                       font=("SF Pro Display", 14),
                                       dropdown_font=("SF Pro Display", 14))
        self.reg_role.set("Coder")
        self.reg_role.pack(pady=(0, 30))

        btn_register = ctk.CTkButton(form_frame, text="Hesap Oluştur",
                                     command=self.handle_register,
                                     width=340, height=48,
                                     corner_radius=12,
                                     fg_color=COLORS['accent_secondary'],
                                     hover_color="#4a9e4a",
                                     font=("SF Pro Display", 14, "bold"))
        btn_register.pack(pady=(0, 20))

        ctk.CTkButton(form_frame, text="Giriş Ekranına Dön",
                     fg_color="transparent",
                     hover_color=COLORS['hover'],
                     text_color=COLORS['text_secondary'],
                     font=("SF Pro Display", 12),
                     command=self.show_login_frame,
                     height=30).pack()

    def show_forgot_password_dialog(self):
        """Şifremi Unuttum dialog penceresi"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Şifre Sıfırlama")
        dialog.geometry("500x450")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS['bg_primary'])

        header = ctk.CTkFrame(dialog, fg_color=COLORS['bg_secondary'], height=70)
        header.pack(fill="x", padx=0, pady=0)
        ctk.CTkLabel(header, text="🔐 Şifre Sıfırlama",
                    font=("SF Pro Display", 22, "bold"),
                    text_color=COLORS['text_primary']).pack(pady=20)

        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(main_frame, text="Email adresinizi girin. Şifre sıfırlama kodu email adresinize gönderilecektir.",
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_secondary'],
                    wraplength=400,
                    justify="left").pack(pady=(0, 20))

        # Email girişi
        ctk.CTkLabel(main_frame, text="Email Adresi",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_email = ctk.CTkEntry(main_frame, placeholder_text="email@example.com",
                                  width=440, height=44,
                                  corner_radius=10, border_width=1,
                                  border_color=COLORS['border'],
                                  font=("SF Pro Display", 13))
        entry_email.pack(fill="x", pady=(0, 20))

        # Token girişi (gizli başlangıçta)
        token_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        token_frame.pack(fill="x", pady=(0, 20))
        token_frame.pack_forget()

        ctk.CTkLabel(token_frame, text="Şifre Sıfırlama Kodu (6 haneli)",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_token = ctk.CTkEntry(token_frame, placeholder_text="000000",
                                   width=440, height=50,
                                   corner_radius=10, border_width=2,
                                   border_color=COLORS['accent_primary'],
                                   font=("SF Pro Display", 24, "bold"),
                                   justify="center")
        entry_token.pack(fill="x", pady=(0, 12))

        # Sadece rakam girişi için validasyon
        def validate_code_input(char):
            return char.isdigit() or char == ""
        entry_token.configure(validate="key", validatecommand=(entry_token.register(validate_code_input), "%S"))

        # Maksimum 6 karakter
        def limit_length(event):
            if len(entry_token.get()) > 6:
                entry_token.delete(6, "end")
        entry_token.bind("<KeyRelease>", limit_length)

        # Yeni şifre (gizli başlangıçta)
        password_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        password_frame.pack(fill="x", pady=(0, 20))
        password_frame.pack_forget()  # Başlangıçta gizli

        ctk.CTkLabel(password_frame, text="Yeni Şifre",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_new_pass = ctk.CTkEntry(password_frame, placeholder_text="Yeni şifrenizi girin",
                                      show="*", width=440, height=44,
                                      corner_radius=10, border_width=1,
                                      border_color=COLORS['border'],
                                      font=("SF Pro Display", 13))
        entry_new_pass.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(password_frame, text="Yeni Şifre (Tekrar)",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_confirm_pass = ctk.CTkEntry(password_frame, placeholder_text="Yeni şifrenizi tekrar girin",
                                          show="*", width=440, height=44,
                                          corner_radius=10, border_width=1,
                                          border_color=COLORS['border'],
                                          font=("SF Pro Display", 13))
        entry_confirm_pass.pack(fill="x")

        # Durum mesajı
        status_label = ctk.CTkLabel(main_frame, text="",
                                    font=("SF Pro Display", 12),
                                    text_color=COLORS['accent_secondary'],
                                    wraplength=400,
                                    justify="left")
        status_label.pack(pady=(0, 20))

        # Butonlar
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=20)

        def send_reset_code():
            email = entry_email.get().strip()
            if not email:
                status_label.configure(text="Lütfen email adresinizi girin.",
                                      text_color=COLORS['accent_danger'])
                return

            # Yükleme durumu göster
            status_label.configure(text="Email gönderiliyor, lütfen bekleyin...",
                                  text_color=COLORS['text_secondary'])
            dialog.update()

            try:
                success, msg = self.db.request_password_reset(email)
                if success:
                    status_label.configure(text=msg, text_color=COLORS['accent_secondary'])
                    entry_email.configure(state="disabled")
                    token_frame.pack(fill="x", pady=(0, 20))
                    btn_send.pack_forget()
                    btn_verify.pack(side="left", padx=(0, 10))
                else:
                    status_label.configure(text=f"❌ {msg}", text_color=COLORS['accent_danger'])
                    messagebox.showerror("Hata", msg)
            except Exception as e:
                error_msg = f"Hata oluştu: {str(e)}"
                status_label.configure(text=f"❌ {error_msg}",
                                      text_color=COLORS['accent_danger'])
                messagebox.showerror("Hata", error_msg)
                import traceback
                print(f"Şifre sıfırlama hatası: {traceback.format_exc()}")

        def verify_token():
            token = entry_token.get().strip()
            if not token:
                status_label.configure(text="Lütfen şifre sıfırlama kodunu girin.",
                                      text_color=COLORS['accent_danger'])
                return

            if len(token) != 6 or not token.isdigit():
                status_label.configure(text="Kod 6 haneli rakam olmalıdır. (Örnek: 123456)",
                                      text_color=COLORS['accent_danger'])
                return

            valid, user_id, msg = self.db.verify_reset_token(token)
            if valid:
                status_label.configure(text="Kod doğrulandı. Yeni şifrenizi girin.",
                                      text_color=COLORS['accent_secondary'])
                entry_token.configure(state="disabled")
                password_frame.pack(fill="x", pady=(0, 20))
                btn_verify.pack_forget()
                btn_reset.pack(side="left", padx=(0, 10))
            else:
                status_label.configure(text=msg, text_color=COLORS['accent_danger'])

        def reset_password():
            token = entry_token.get().strip()
            new_pass = entry_new_pass.get()
            confirm_pass = entry_confirm_pass.get()

            if not new_pass or not confirm_pass:
                status_label.configure(text="Lütfen yeni şifrenizi girin.",
                                      text_color=COLORS['accent_danger'])
                return

            if new_pass != confirm_pass:
                status_label.configure(text="Şifreler eşleşmiyor. Lütfen tekrar deneyin.",
                                      text_color=COLORS['accent_danger'])
                return

            if len(new_pass) < 6:
                status_label.configure(text="Şifre en az 6 karakter olmalıdır.",
                                      text_color=COLORS['accent_danger'])
                return

            success, msg = self.db.reset_password(token, new_pass)
            if success:
                status_label.configure(text=msg, text_color=COLORS['accent_secondary'])
                messagebox.showinfo("Başarılı", "Şifreniz başarıyla güncellendi.\n\nGiriş sayfasına yönlendiriliyorsunuz...")
                dialog.destroy()
                self.show_login_frame()
            else:
                status_label.configure(text=msg, text_color=COLORS['accent_danger'])

        btn_send = ctk.CTkButton(btn_frame, text="Kod Gönder",
                                command=send_reset_code,
                                width=140, height=40,
                                corner_radius=10,
                                fg_color=COLORS['accent_primary'],
                                hover_color="#3a8eef",
                                font=("SF Pro Display", 13, "bold"))
        btn_send.pack(side="left", padx=(0, 10))

        btn_verify = ctk.CTkButton(btn_frame, text="Kodu Doğrula",
                                   command=verify_token,
                                   width=140, height=40,
                                   corner_radius=10,
                                   fg_color=COLORS['accent_secondary'],
                                   hover_color="#4a9e4a",
                                   font=("SF Pro Display", 13, "bold"))
        btn_verify.pack_forget()  # Başlangıçta gizli

        btn_reset = ctk.CTkButton(btn_frame, text="Şifreyi Sıfırla",
                                  command=reset_password,
                                  width=140, height=40,
                                  corner_radius=10,
                                  fg_color=COLORS['accent_secondary'],
                                  hover_color="#4a9e4a",
                                  font=("SF Pro Display", 13, "bold"))
        btn_reset.pack_forget()  # Başlangıçta gizli

        btn_close = ctk.CTkButton(btn_frame, text="Kapat",
                                 command=dialog.destroy,
                                 width=100, height=40,
                                 corner_radius=10,
                                 fg_color="transparent",
                                 hover_color=COLORS['hover'],
                                 border_width=1,
                                 border_color=COLORS['border'],
                                 font=("SF Pro Display", 13))
        btn_close.pack(side="right")

    def handle_login(self):
        u_name = self.entry_user.get()
        p_word = self.entry_pass.get()

        success, user_data = self.db.login_user(u_name, p_word)

        if success:
            # user_data: (id, username, email) şeklinde gelir
            self.current_user_id = user_data[0]
            self.current_username = user_data[1]
            messagebox.showinfo("Giriş Başarılı",
                               f"Hoş geldiniz, {self.current_username}!\n\nYönetim paneline yönlendiriliyorsunuz.")
            self.show_dashboard()  # DASHBOARD'A GİDİYORUZ
        else:
            messagebox.showerror("Giriş Hatası",
                                "Giriş başarısız.\n\nKullanıcı adı veya şifre hatalı. Lütfen bilgilerinizi kontrol edip tekrar deneyin.")

    def handle_register(self):
        u_name = self.reg_user.get()
        p_word = self.reg_pass.get()
        email = self.reg_email.get()
        role = self.reg_role.get()

        if not u_name or not p_word:
            messagebox.showwarning("Eksik Bilgi",
                                   "Lütfen tüm zorunlu alanları doldurun.\n\nKullanıcı adı ve şifre gereklidir.")
            return

        # Email validation
        if email and not validate_email(email):
            messagebox.showerror("Geçersiz Email Formatı",
                                "Girdiğiniz email adresi geçerli bir formatta değil.\n\n"
                                "Lütfen doğru bir email adresi girin.\nÖrnek: kullanici@example.com")
            return

        success, message = self.db.register_user(u_name, p_word, email,)

        if success:
            messagebox.showinfo("Kayıt Başarılı",
                               f"Hesabınız başarıyla oluşturuldu.\n\n{message}\n\nGiriş sayfasına yönlendiriliyorsunuz.")
            self.show_login_frame()
        else:
            messagebox.showerror("Kayıt Hatası",
                                 f"Kayıt işlemi tamamlanamadı.\n\n{message}\n\nLütfen bilgilerinizi kontrol edip tekrar deneyin.")

    def show_dashboard(self):
        """Ana Yönetim Paneli"""
        for widget in self.winfo_children():
            widget.destroy()

        # --- SOL MENÜ (SIDEBAR) ---
        self.sidebar = ctk.CTkFrame(self, width=260, corner_radius=0,
                                   fg_color=COLORS['bg_secondary'], border_width=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # Logo/Başlık Alanı
        header_sidebar = ctk.CTkFrame(self.sidebar, fg_color="transparent", height=80)
        header_sidebar.pack(fill="x", padx=20, pady=(30, 20))
        ctk.CTkLabel(header_sidebar, text="Startup Platform",
                    font=("SF Pro Display", 18, "bold"),
                    text_color=COLORS['text_primary']).pack()

        # Kullanıcı Bilgisi
        user_info = ctk.CTkFrame(self.sidebar, fg_color=COLORS['bg_tertiary'],
                                corner_radius=12, height=60)
        user_info.pack(fill="x", padx=15, pady=(0, 25))
        ctk.CTkLabel(user_info, text=f"👤 {self.current_username}",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_primary']).pack(pady=15)

        # Bölüm Başlığı
        ctk.CTkLabel(self.sidebar, text="TAKIMLARIM",
                    font=("SF Pro Display", 11, "bold"),
                    text_color=COLORS['text_muted']).pack(anchor="w", padx=20, pady=(0, 12))

        # Takım Listesi
        teams_frame = ctk.CTkScrollableFrame(self.sidebar, fg_color="transparent")
        teams_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        my_teams = self.db.get_user_teams(self.current_user_id)
        for team in my_teams:
            btn = ctk.CTkButton(teams_frame, text=f"📂 {team[1]}",
                                fg_color="transparent",
                                hover_color=COLORS['hover'],
                                border_width=1,
                                border_color=COLORS['border'],
                                corner_radius=10,
                                height=42,
                                font=("SF Pro Display", 13),
                                anchor="w",
                                command=lambda t_id=team[0], t_name=team[1]: self.show_team_page(t_id, t_name))
            btn.pack(fill="x", pady=4)

        # Alt Butonlar
        bottom_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        bottom_frame.pack(fill="x", padx=15, pady=15, side="bottom")

        ctk.CTkButton(bottom_frame, text="+ Yeni Takım",
                     fg_color=COLORS['accent_secondary'],
                     hover_color="#4a9e4a",
                     height=40,
                     corner_radius=10,
                     font=("SF Pro Display", 13, "bold"),
                     command=self.open_create_team_popup).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(bottom_frame, text="📩 Davetler",
                     fg_color=COLORS['bg_tertiary'],
                     hover_color=COLORS['hover'],
                     height=40,
                     corner_radius=10,
                     font=("SF Pro Display", 13),
                     command=self.show_invites_page).pack(fill="x", pady=(0, 10))

        ctk.CTkButton(bottom_frame, text="Çıkış Yap",
                     fg_color="transparent",
                     hover_color=COLORS['hover'],
                     text_color=COLORS['accent_danger'],
                     border_width=1,
                     border_color=COLORS['accent_danger'],
                     height=40,
                     corner_radius=10,
                     font=("SF Pro Display", 13),
                     command=self.show_login_frame).pack(fill="x")

        # --- SAĞ İÇERİK ALANI ---
        self.content_area = ctk.CTkFrame(self, corner_radius=0,
                                        fg_color=COLORS['bg_primary'], border_width=0)
        self.content_area.pack(side="right", fill="both", expand=True)

        # Boş Durum
        empty_frame = ctk.CTkFrame(self.content_area, fg_color="transparent")
        empty_frame.pack(expand=True)
        ctk.CTkLabel(empty_frame, text="👈", font=("SF Pro Display", 48)).pack(pady=(0, 20))
        ctk.CTkLabel(empty_frame, text="Bir takım seçin",
                    font=("SF Pro Display", 24, "bold"),
                    text_color=COLORS['text_primary']).pack(pady=(0, 10))
        ctk.CTkLabel(empty_frame, text="Soldan bir takım seçin veya yeni takım oluşturun",
                    font=("SF Pro Display", 14),
                    text_color=COLORS['text_secondary']).pack()

    def show_team_page(self, team_id, team_name):
        """Seçilen takımın detaylarını ve görevlerini gösterir"""
        # Sağ tarafı temizle
        for widget in self.content_area.winfo_children():
            widget.destroy()

        # Üst Başlık
        header = ctk.CTkFrame(self.content_area, height=70, fg_color="transparent")
        header.pack(fill="x", padx=30, pady=(30, 20))

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        ctk.CTkLabel(title_frame, text=team_name,
                    font=("SF Pro Display", 28, "bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w")
        ctk.CTkLabel(title_frame, text="Takım Yönetimi",
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_secondary']).pack(anchor="w", pady=(5, 0))

        # Üye Davet Et Butonu
        ctk.CTkButton(header, text="+ Üye Davet Et",
                     width=140, height=40,
                     corner_radius=10,
                     fg_color=COLORS['accent_primary'],
                     hover_color="#3a8eef",
                     font=("SF Pro Display", 13, "bold"),
                     command=lambda: self.open_invite_popup(team_id)).pack(side="right", padx=(10, 0))

        # --- GÖREV EKLEME ALANI --- (Kompakt)
        task_control = ctk.CTkFrame(self.content_area,
                                   fg_color=COLORS['bg_secondary'],
                                   corner_radius=12,
                                   border_width=1,
                                   border_color=COLORS['border'])
        task_control.pack(fill="x", padx=30, pady=(20, 16))

        # Kompakt form - tek satır
        form_row = ctk.CTkFrame(task_control, fg_color="transparent")
        form_row.pack(fill="x", padx=16, pady=12)

        # Başlık (küçük)
        self.entry_task_title = ctk.CTkEntry(form_row, placeholder_text="Görev başlığı",
                                            width=220, height=36,
                                            corner_radius=8, border_width=1,
                                            border_color=COLORS['border'],
                                            font=("SF Pro Display", 12))
        self.entry_task_title.pack(side="left", padx=(0, 10))

        # Tarih (küçük)
        self.entry_task_date = ctk.CTkEntry(form_row, placeholder_text="YYYY-MM-DD",
                                           width=110, height=36,
                                           corner_radius=8, border_width=1,
                                           border_color=COLORS['border'],
                                           font=("SF Pro Display", 12))
        self.entry_task_date.pack(side="left", padx=(0, 10))

        # Görevi kime atayacağız?
        members = self.db.get_team_members(team_id)  # [(id, username, role), ...]

        # Atanacak kişiler (kompakt - ilk 3 kişi görünür)
        assign_frame = ctk.CTkFrame(form_row, fg_color="transparent")
        assign_frame.pack(side="left", padx=(0, 10))

        self.assign_checkboxes = {}
        # İlk 3 kişiyi göster
        max_visible = min(3, len(members))
        for i, (member_id, member_name, role) in enumerate(members[:max_visible]):
            var = ctk.BooleanVar(value=False)
            cb = ctk.CTkCheckBox(assign_frame, text=member_name,
                               variable=var,
                               font=("SF Pro Display", 11),
                               corner_radius=5)
            cb.pack(side="left", padx=(0, 8))
            self.assign_checkboxes[member_id] = var

        # Eğer 3'ten fazla kişi varsa, kalanları da ekle (görünmez checkbox'lar)
        if len(members) > max_visible:
            more_label = ctk.CTkLabel(assign_frame, text=f"+{len(members) - max_visible}",
                                     font=("SF Pro Display", 11),
                                     text_color=COLORS['text_muted'])
            more_label.pack(side="left", padx=(0, 8))
            # Kalan kişileri de checkbox'lara ekle (görünmez ama seçilebilir)
            for member_id, member_name, role in members[max_visible:]:
                var = ctk.BooleanVar(value=False)
                self.assign_checkboxes[member_id] = var

        # Açıklama (opsiyonel, küçük)
        self.entry_task_desc = ctk.CTkEntry(form_row, placeholder_text="Açıklama (opsiyonel)",
                                           width=160, height=36,
                                           corner_radius=8, border_width=1,
                                           border_color=COLORS['border'],
                                           font=("SF Pro Display", 11))
        self.entry_task_desc.pack(side="left", padx=(0, 10))

        # Buton (küçük)
        btn_add_task = ctk.CTkButton(form_row, text="+ Ekle",
                                     width=70, height=36,
                                     corner_radius=8,
                                     fg_color=COLORS['accent_secondary'],
                                     hover_color="#4a9e4a",
                                     font=("SF Pro Display", 12, "bold"),
                                     command=lambda: self.add_task_action(team_id, members))
        btn_add_task.pack(side="right")

        # --- GÖREV LİSTESİ --- (Daha görünür ve büyük)
        tasks_section = ctk.CTkFrame(self.content_area,
                                    fg_color=COLORS['bg_secondary'],
                                    corner_radius=20,
                                    border_width=1,
                                    border_color=COLORS['border'])
        tasks_section.pack(fill="both", expand=True, padx=30, pady=(0, 30))

        # Görevler başlığı (Daha büyük ve vurgulu)
        tasks_header = ctk.CTkFrame(tasks_section, fg_color="transparent")
        tasks_header.pack(fill="x", padx=28, pady=(28, 24))

        title_frame = ctk.CTkFrame(tasks_header, fg_color="transparent")
        title_frame.pack(side="left", fill="y")
        ctk.CTkLabel(title_frame, text="📋 Görevler",
                    font=("SF Pro Display", 28, "bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w")

        # Görevleri getir (bir kez)
        tasks = self.db.get_team_tasks(team_id)

        # Görev sayısı (Daha büyük)
        task_count = len(tasks) if tasks else 0
        count_label = ctk.CTkLabel(title_frame, text=f"{task_count} görev",
                    font=("SF Pro Display", 15),
                    text_color=COLORS['text_secondary'])
        count_label.pack(anchor="w", pady=(6, 0))

        # Görev filtreleme ve sıralama kontrolleri
        filter_frame = ctk.CTkFrame(tasks_section, fg_color="transparent")
        filter_frame.pack(fill="x", padx=28, pady=(0, 16))

        # Durum filtresi
        ctk.CTkLabel(filter_frame, text="Filtre:",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary']).pack(side="left", padx=(0, 10))

        status_filter_var = ctk.StringVar(value="Tümü")
        status_filter = ctk.CTkComboBox(filter_frame,
                                       values=["Tümü", "Todo", "In Progress", "Done"],
                                       variable=status_filter_var,
                                       width=150, height=36,
                                       corner_radius=8,
                                       font=("SF Pro Display", 12))
        status_filter.pack(side="left", padx=(0, 10))

        # Sıralama
        ctk.CTkLabel(filter_frame, text="Sırala:",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary']).pack(side="left", padx=(20, 10))

        sort_var = ctk.StringVar(value="Tarih (Yeni)")
        sort_combo = ctk.CTkComboBox(filter_frame,
                                    values=["Tarih (Yeni)", "Tarih (Eski)", "Başlık (A-Z)", "Başlık (Z-A)", "Durum"],
                                    variable=sort_var,
                                    width=150, height=36,
                                    corner_radius=8,
                                    font=("SF Pro Display", 12))
        sort_combo.pack(side="left")

        scroll_frame = ctk.CTkScrollableFrame(tasks_section,
                                             fg_color="transparent",
                                             label_text="")
        scroll_frame.pack(fill="both", expand=True, padx=28, pady=(0, 28))

        # Görevleri filtrele ve sırala
        def filter_and_sort_tasks():
            # Scroll frame'i temizle
            for widget in scroll_frame.winfo_children():
                widget.destroy()

            filtered_tasks = tasks.copy() if tasks else []

            # Durum filtresi
            if status_filter_var.get() != "Tümü":
                filtered_tasks = [t for t in filtered_tasks if t[3] == status_filter_var.get()]

            # Sıralama
            if sort_var.get() == "Tarih (Yeni)":
                filtered_tasks = sorted(filtered_tasks, key=lambda x: x[0], reverse=True)
            elif sort_var.get() == "Tarih (Eski)":
                filtered_tasks = sorted(filtered_tasks, key=lambda x: x[0])
            elif sort_var.get() == "Başlık (A-Z)":
                filtered_tasks = sorted(filtered_tasks, key=lambda x: x[1].lower())
            elif sort_var.get() == "Başlık (Z-A)":
                filtered_tasks = sorted(filtered_tasks, key=lambda x: x[1].lower(), reverse=True)
            elif sort_var.get() == "Durum":
                status_order = {"Todo": 0, "In Progress": 1, "Done": 2}
                filtered_tasks = sorted(filtered_tasks, key=lambda x: status_order.get(x[3], 3))

            # Görev sayısını güncelle
            count_label.configure(text=f"{len(filtered_tasks)} görev")

            # Görevleri göster
            if not filtered_tasks:
                empty_tasks = ctk.CTkFrame(scroll_frame, fg_color="transparent")
                empty_tasks.pack(expand=True, pady=60)
                ctk.CTkLabel(empty_tasks, text="🔍", font=("SF Pro Display", 48)).pack(pady=(0, 16))
                ctk.CTkLabel(empty_tasks, text="Filtreye uygun görev bulunamadı",
                            font=("SF Pro Display", 18, "bold"),
                            text_color=COLORS['text_primary']).pack(pady=(0, 8))
                ctk.CTkLabel(empty_tasks, text="Filtre ayarlarını değiştirerek tekrar deneyin",
                            font=("SF Pro Display", 13),
                            text_color=COLORS['text_secondary']).pack()
            else:
                display_tasks(filtered_tasks)

        # Görevleri gösteren fonksiyon
        def display_tasks(task_list):
            for task in task_list:
                # task: (id, title, desc, status, deadline, assigned_names_list, created_by_id)
                task_id = task[0]
                task_title = task[1]
                task_desc = task[2] if task[2] else "Açıklama yok"
                task_status = task[3]
                task_deadline = task[4]
                assigned_users = task[5] if task[5] else ["Atanmamış"]
                assigned_user_text = ", ".join(assigned_users) if isinstance(assigned_users, list) else assigned_users
                created_by_id = task[6]  # Görevi oluşturan kişi ID'si
                is_creator = (created_by_id == self.current_user_id)  # Mevcut kullanıcı görevi oluşturan mı?

                card = ctk.CTkFrame(scroll_frame,
                                  fg_color=COLORS['bg_tertiary'],
                                  corner_radius=16,
                                  border_width=1,
                                  border_color=COLORS['border'],
                                  cursor="hand2")
                card.pack(fill="x", pady=10)

                # Kart tıklanabilir - detay penceresi açar
                def on_card_click(event, tid=task_id):
                    # Butonlara tıklama olayını engelle
                    widget_under = event.widget
                    if isinstance(widget_under, ctk.CTkButton):
                        return
                    self.show_task_detail(tid, team_id, team_name, members)

                # Kart'a hover efekti ekle
                def on_enter(event):
                    card.configure(border_color=COLORS['accent_primary'], border_width=2)
                def on_leave(event):
                    card.configure(border_color=COLORS['border'], border_width=1)

                card.bind("<Enter>", on_enter)
                card.bind("<Leave>", on_leave)
                card.bind("<Button-1>", lambda e: on_card_click(e))
                card.configure(cursor="hand2")

                # Sol taraf: Görev bilgileri (tıklanabilir)
                left_frame = ctk.CTkFrame(card, fg_color="transparent")
                left_frame.pack(side="left", fill="both", expand=True, padx=24, pady=22)
                left_frame.bind("<Button-1>", lambda e: on_card_click(e))
                left_frame.configure(cursor="hand2")

                # Başlık (Daha büyük ve vurgulu)
                title_label = ctk.CTkLabel(left_frame, text=task_title,
                                          font=("SF Pro Display", 20, "bold"),
                                          text_color=COLORS['text_primary'],
                                          anchor="w",
                                          cursor="hand2")
                title_label.pack(fill="x", pady=(0, 12))
                title_label.bind("<Button-1>", lambda e: on_card_click(e))

                # Açıklama (Daha görünür ve tıklanabilir)
                if task_desc and task_desc != "Açıklama yok":
                    # Açıklamayı kısalt (çok uzunsa)
                    desc_preview = task_desc[:150] + "..." if len(task_desc) > 150 else task_desc
                    desc_label = ctk.CTkLabel(left_frame, text=desc_preview,
                                             font=("SF Pro Display", 14),
                                             text_color=COLORS['text_secondary'],
                                             anchor="w",
                                             wraplength=550,
                                             justify="left",
                                             cursor="hand2")
                    desc_label.pack(fill="x", pady=(0, 12))
                    desc_label.bind("<Button-1>", lambda e: on_card_click(e))

                # Bilgiler (Daha büyük ve görünür, tıklanabilir)
                info_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
                info_frame.pack(fill="x")
                info_frame.bind("<Button-1>", lambda e: on_card_click(e))
                info_frame.configure(cursor="hand2")

                assigned_label = ctk.CTkLabel(info_frame, text=f"👤 {assigned_user_text}",
                            font=("SF Pro Display", 14, "bold"),
                            text_color=COLORS['text_secondary'],
                            cursor="hand2")
                assigned_label.pack(side="left", padx=(0, 24))
                assigned_label.bind("<Button-1>", lambda e: on_card_click(e))

                deadline_label = ctk.CTkLabel(info_frame, text=f"📅 {task_deadline}",
                            font=("SF Pro Display", 14, "bold"),
                            text_color=COLORS['text_secondary'],
                            cursor="hand2")
                deadline_label.pack(side="left")
                deadline_label.bind("<Button-1>", lambda e: on_card_click(e))

                # Tıklanabilir olduğunu gösteren ipucu
                hint_label = ctk.CTkLabel(left_frame, text="💡 Detaylar için tıklayın",
                                         font=("SF Pro Display", 11),
                                         text_color=COLORS['text_muted'],
                                         cursor="hand2")
                hint_label.pack(anchor="w", pady=(8, 0))
                hint_label.bind("<Button-1>", lambda e: on_card_click(e))

                # Sağ taraf: Durum ve butonlar
                right_frame = ctk.CTkFrame(card, fg_color="transparent")
                right_frame.pack(side="right", padx=24, pady=22)

                # Durum etiketi
                status_colors = {
                    "Todo": ("#ff9800", COLORS['bg_tertiary']),
                    "In Progress": (COLORS['accent_primary'], COLORS['bg_tertiary']),
                    "Done": (COLORS['accent_secondary'], COLORS['bg_tertiary'])
                }
                status_color, status_bg = status_colors.get(task_status, (COLORS['text_muted'], COLORS['bg_tertiary']))

                status_badge = ctk.CTkFrame(right_frame,
                                          fg_color=status_bg,
                                          corner_radius=10,
                                          width=120)
                status_badge.pack(pady=(0, 18))
                ctk.CTkLabel(status_badge, text=task_status,
                            text_color=status_color,
                            font=("SF Pro Display", 12, "bold")).pack(padx=14, pady=8)

                # Butonlar - Dikey yerleşim, modern tasarım
                btn_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
                btn_frame.pack()

                # Detay görüntüleme butonu (herkes için)
                btn_view = ctk.CTkButton(btn_frame, text="👁️ Detay",
                                        width=120, height=40,
                                        fg_color=COLORS['accent_primary'],
                                        hover_color="#3a8eef",
                                        border_width=0,
                                        font=("SF Pro Display", 13, "bold"),
                                        command=lambda tid=task_id: self.show_task_detail(tid, team_id, team_name, members),
                                        corner_radius=10)
                btn_view.pack(pady=5)

                if task_status != "Done":
                    btn_done = ctk.CTkButton(btn_frame, text="✓ Tamamla",
                                            width=120, height=40,
                                            fg_color=COLORS['accent_secondary'],
                                            hover_color="#4a9e4a",
                                            border_width=0,
                                            font=("SF Pro Display", 13, "bold"),
                                            command=lambda tid=task_id: self.complete_task_action(tid, team_id, team_name),
                                            corner_radius=10)
                    btn_done.pack(pady=5)

                # Düzenleme ve silme butonları sadece görevi oluşturan kişiye gösterilir
                if is_creator:
                    btn_edit = ctk.CTkButton(btn_frame, text="✎ Düzenle",
                                            width=120, height=40,
                                            fg_color="transparent",
                                            hover_color=COLORS['hover'],
                                            border_width=1,
                                            border_color=COLORS['border'],
                                            text_color=COLORS['text_primary'],
                                            font=("SF Pro Display", 13),
                                            command=lambda tid=task_id: self.show_task_detail(tid, team_id, team_name, members, edit_mode=True),
                                            corner_radius=10)
                    btn_edit.pack(pady=5)

                    btn_delete = ctk.CTkButton(btn_frame, text="× Sil",
                                              width=120, height=40,
                                              fg_color="transparent",
                                              hover_color=COLORS['hover'],
                                              border_width=1,
                                              border_color=COLORS['accent_danger'],
                                              text_color=COLORS['accent_danger'],
                                              font=("SF Pro Display", 13),
                                              command=lambda tid=task_id: self.delete_task_action(tid, team_id, team_name),
                                              corner_radius=10)
                    btn_delete.pack(pady=5)

        # Filtre ve sıralama değişikliklerini dinle
        status_filter_var.trace("w", lambda *args: filter_and_sort_tasks())
        sort_var.trace("w", lambda *args: filter_and_sort_tasks())

        # İlk yüklemede görevleri göster
        filter_and_sort_tasks()

    def add_task_action(self, team_id, members_data):
        """Görevi veritabanına kaydeder (çoklu atama ile)"""
        title = self.entry_task_title.get()
        deadline = self.entry_task_date.get()
        description = self.entry_task_desc.get() or "Açıklama yok"

        if not title or not deadline:
            messagebox.showwarning("Eksik Bilgi",
                                   "Lütfen tüm zorunlu alanları doldurun.\n\nGörev başlığı ve son tarih gereklidir.")
            return

        # Seçili CheckBox'ları bul
        assigned_ids = []
        assigned_names = []
        for member_id, var in self.assign_checkboxes.items():
            if var.get():
                assigned_ids.append(member_id)
                # İsim bul
                for m in members_data:
                    if m[0] == member_id:
                        assigned_names.append(m[1])
                        break

        if not assigned_ids:
            messagebox.showwarning("Eksik Bilgi",
                                   "Lütfen en az bir kişi seçin.\n\nGörevi atamak için en az bir kişi seçmelisiniz.")
            return

        self.db.create_task(team_id, title, description, assigned_ids, deadline, self.current_user_id)
        assigned_text = ", ".join(assigned_names)
        messagebox.showinfo("Görev Oluşturuldu",
                           f"Görev başarıyla oluşturuldu.\n\nBaşlık: {title}\nAtanan: {assigned_text}")
        # Formu temizle
        self.entry_task_title.delete(0, "end")
        self.entry_task_date.delete(0, "end")
        self.entry_task_desc.delete(0, "end")
        # CheckBox'ları temizle
        for var in self.assign_checkboxes.values():
            var.set(False)
        # Sayfayı yenile ki yeni görev görünsün
        # team_name'i instance variable'dan al
        if hasattr(self, 'current_team_name'):
            self.show_team_page(team_id, self.current_team_name)
        else:
            # Fallback: team_name'i header'dan al
            try:
                header = self.content_area.winfo_children()[0]
                team_name = header.winfo_children()[0].cget("text")
                self.show_team_page(team_id, team_name)
            except:
                # Son çare: direkt team_id ile yeniden yükle
                self.show_team_page(team_id, f"Takım {team_id}")

    def open_invite_popup(self, team_id):
        """Kullanıcı adı ile davet gönderme"""
        dialog = ctk.CTkInputDialog(text="Davet edilecek Kullanıcı Adı:", title="Üye Ekle")
        target_user = dialog.get_input()
        if target_user:
            success, msg = self.db.send_invite(self.current_user_id, target_user, team_id)
            if success:
                messagebox.showinfo("Davet Gönderildi",
                                   f"Takım daveti başarıyla gönderildi.\n\n{msg}")
            else:
                messagebox.showerror("Davet Hatası",
                                    f"Davet gönderilemedi.\n\n{msg}\n\nLütfen bilgileri kontrol edip tekrar deneyin.")

    def open_create_team_popup(self):
        """Basit bir takım kurma penceresi"""
        dialog = ctk.CTkInputDialog(text="Takımının Adı Ne Olsun?", title="Takım Kur")
        team_name = dialog.get_input()
        if team_name:
            # Deadline parametresi eksikti - None olarak geçiyoruz (opsiyonel)
            self.db.create_team(team_name, "Açıklama yok", self.current_user_id, None)
            messagebox.showinfo("Takım Oluşturuldu",
                               f"'{team_name}' takımı başarıyla oluşturuldu.\n\nArtık takımınıza üye ekleyebilir ve görevler oluşturabilirsiniz.")
            # Dashboard'ı yenile ki yeni takım görünsün
            self.show_dashboard()

    def show_invites_page(self):
        """Gelen davetleri sağ tarafta listeler"""
        # Önce sağ tarafı temizle
        for widget in self.content_area.winfo_children():
            widget.destroy()

        ctk.CTkLabel(self.content_area, text="Gelen Davetler", font=("Arial", 18, "bold")).pack(pady=10)

        invites = self.db.get_my_invites(self.current_user_id)

        if not invites:
            ctk.CTkLabel(self.content_area, text="Henüz bir davetin yok.").pack(pady=20)

        for inv in invites:
            # inv: (id, gonderen, takim, mesaj, team_id)
            card = ctk.CTkFrame(self.content_area, fg_color="#444")
            card.pack(fill="x", pady=5, padx=10)

            lbl = ctk.CTkLabel(card, text=f"{inv[1]} seni '{inv[2]}' takımına çağırıyor!", font=("Arial", 14))
            lbl.pack(side="left", padx=10)

            # Kabul Et Butonu
            btn_accept = ctk.CTkButton(card, text="Kabul Et", width=80, fg_color="green",
                                       command=lambda i=inv[0]: self.accept_invite_action(i))
            btn_accept.pack(side="right", padx=5, pady=5)

    def accept_invite_action(self, invite_id):
        self.db.respond_invite(invite_id, accept=True)
        messagebox.showinfo("Davet Kabul Edildi",
                           "Takım daveti başarıyla kabul edildi.\n\nArtık bu takımın görevlerini görüntüleyebilir ve katkıda bulunabilirsiniz.")
        self.show_invites_page()  # Sayfayı yenile

    def complete_task_action(self, task_id, team_id, team_name):
        """Görevi tamamlandı olarak işaretler"""
        result = messagebox.askyesno("Görev Tamamlama",
                                     "Bu görevi tamamlandı olarak işaretlemek istediğinize emin misiniz?")
        if result:
            self.db.mark_task_done(task_id, self.current_user_id)
            messagebox.showinfo("Görev Tamamlandı",
                               "Görev başarıyla tamamlandı olarak işaretlendi.\n\nGörev listesi güncelleniyor.")
            self.show_team_page(team_id, team_name)

    def delete_task_action(self, task_id, team_id, team_name):
        """Görevi siler"""
        result = messagebox.askyesno("Görev Silme Onayı",
                                     "Bu görevi silmek istediğinize emin misiniz?\n\nBu işlem geri alınamaz.")
        if result:
            self.db.delete_task(task_id)
            messagebox.showinfo("Görev Silindi",
                               "Görev başarıyla silindi.\n\nGörev listesi güncelleniyor.")
            # team_name'i instance variable'dan al
            if hasattr(self, 'current_team_name'):
                self.show_team_page(team_id, self.current_team_name)
            else:
                self.show_team_page(team_id, team_name)

    def show_task_detail(self, task_id, team_id, team_name, members, edit_mode=False):
        """Görev detay görüntüleme penceresi"""
        # Görev bilgilerini getir
        task = self.db.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Görev Bulunamadı",
                                "Seçilen görev bulunamadı.\n\nGörev silinmiş veya erişim yetkiniz olmayabilir.")
            return

        # task: (id, title, description, status, deadline, assigned_user_ids, assigned_user_names, created_by_id, created_by_username, created_at, team_id)
        task_title = task[1]
        task_desc = task[2] if task[2] else "Açıklama yok"
        task_status = task[3]
        task_deadline = task[4]
        task_assigned_ids = task[5] if task[5] else []
        task_assigned_names = task[6] if task[6] else []
        task_created_by = task[7]
        task_created_by_username = task[8] if task[8] else "Bilinmeyen"
        task_created_at = task[9] if task[9] else "Bilinmiyor"
        is_creator = (task_created_by == self.current_user_id)

        # Dialog penceresi oluştur
        dialog = ctk.CTkToplevel(self)
        dialog.title("Görev Detayları")
        dialog.geometry("700x650")
        dialog.transient(self)
        dialog.grab_set()
        dialog.configure(fg_color=COLORS['bg_primary'])

        # Başlık
        header = ctk.CTkFrame(dialog, fg_color=COLORS['bg_secondary'], height=80)
        header.pack(fill="x", padx=0, pady=0)

        title_frame = ctk.CTkFrame(header, fg_color="transparent")
        title_frame.pack(fill="both", expand=True, padx=30, pady=20)

        ctk.CTkLabel(title_frame, text="📋 Görev Detayları",
                    font=("SF Pro Display", 24, "bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w")

        # Ana içerik (Scrollable)
        main_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=30, pady=20)

        # Görev Başlığı
        title_section = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_secondary'], corner_radius=12)
        title_section.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(title_section, text="Başlık",
                    font=("SF Pro Display", 11, "bold"),
                    text_color=COLORS['text_muted']).pack(anchor="w", padx=20, pady=(16, 8))
        ctk.CTkLabel(title_section, text=task_title,
                    font=("SF Pro Display", 20, "bold"),
                    text_color=COLORS['text_primary']).pack(anchor="w", padx=20, pady=(0, 16))

        # Açıklama
        desc_section = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_secondary'], corner_radius=12)
        desc_section.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(desc_section, text="Açıklama",
                    font=("SF Pro Display", 11, "bold"),
                    text_color=COLORS['text_muted']).pack(anchor="w", padx=20, pady=(16, 8))
        desc_text = ctk.CTkTextbox(desc_section, width=600, height=120,
                                  fg_color=COLORS['bg_tertiary'],
                                  corner_radius=8,
                                  font=("SF Pro Display", 13),
                                  wrap="word")
        desc_text.insert("1.0", task_desc)
        desc_text.configure(state="disabled")
        desc_text.pack(fill="x", padx=20, pady=(0, 16))

        # Bilgiler Grid
        info_section = ctk.CTkFrame(main_frame, fg_color=COLORS['bg_secondary'], corner_radius=12)
        info_section.pack(fill="x", pady=(0, 16))
        ctk.CTkLabel(info_section, text="Görev Bilgileri",
                    font=("SF Pro Display", 11, "bold"),
                    text_color=COLORS['text_muted']).pack(anchor="w", padx=20, pady=(16, 12))

        info_grid = ctk.CTkFrame(info_section, fg_color="transparent")
        info_grid.pack(fill="x", padx=20, pady=(0, 16))

        # Durum
        status_row = ctk.CTkFrame(info_grid, fg_color="transparent")
        status_row.pack(fill="x", pady=8)
        ctk.CTkLabel(status_row, text="Durum:",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_secondary'],
                    width=120).pack(side="left")
        status_colors = {
            "Todo": ("#ff9800", COLORS['bg_tertiary']),
            "In Progress": (COLORS['accent_primary'], COLORS['bg_tertiary']),
            "Done": (COLORS['accent_secondary'], COLORS['bg_tertiary'])
        }
        status_color, status_bg = status_colors.get(task_status, (COLORS['text_muted'], COLORS['bg_tertiary']))
        status_badge = ctk.CTkFrame(status_row, fg_color=status_bg, corner_radius=8, width=120)
        status_badge.pack(side="left")
        ctk.CTkLabel(status_badge, text=task_status,
                    text_color=status_color,
                    font=("SF Pro Display", 12, "bold")).pack(padx=12, pady=6)

        # Son Tarih
        deadline_row = ctk.CTkFrame(info_grid, fg_color="transparent")
        deadline_row.pack(fill="x", pady=8)
        ctk.CTkLabel(deadline_row, text="Son Tarih:",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_secondary'],
                    width=120).pack(side="left")
        ctk.CTkLabel(deadline_row, text=task_deadline if task_deadline else "Belirtilmemiş",
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_primary']).pack(side="left")

        # Atanan Kişiler
        assigned_row = ctk.CTkFrame(info_grid, fg_color="transparent")
        assigned_row.pack(fill="x", pady=8)
        ctk.CTkLabel(assigned_row, text="Atanan Kişiler:",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_secondary'],
                    width=120).pack(side="left", anchor="n")
        assigned_text = ", ".join(task_assigned_names) if task_assigned_names else "Atanmamış"
        ctk.CTkLabel(assigned_row, text=assigned_text,
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_primary'],
                    wraplength=400,
                    justify="left").pack(side="left", fill="x", expand=True)

        # Oluşturan
        creator_row = ctk.CTkFrame(info_grid, fg_color="transparent")
        creator_row.pack(fill="x", pady=8)
        ctk.CTkLabel(creator_row, text="Oluşturan:",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_secondary'],
                    width=120).pack(side="left")
        ctk.CTkLabel(creator_row, text=task_created_by_username,
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_primary']).pack(side="left")

        # Oluşturulma Tarihi
        created_row = ctk.CTkFrame(info_grid, fg_color="transparent")
        created_row.pack(fill="x", pady=8)
        ctk.CTkLabel(created_row, text="Oluşturulma:",
                    font=("SF Pro Display", 13, "bold"),
                    text_color=COLORS['text_secondary'],
                    width=120).pack(side="left")
        created_date = str(task_created_at).split()[0] if task_created_at else "Bilinmiyor"
        ctk.CTkLabel(created_row, text=created_date,
                    font=("SF Pro Display", 13),
                    text_color=COLORS['text_primary']).pack(side="left")

        # Butonlar
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(fill="x", padx=30, pady=20)

        # Sol taraf: İşlem butonları
        left_btns = ctk.CTkFrame(btn_frame, fg_color="transparent")
        left_btns.pack(side="left")

        if task_status != "Done":
            btn_complete = ctk.CTkButton(left_btns, text="✓ Tamamla",
                                        width=120, height=40,
                                        fg_color=COLORS['accent_secondary'],
                                        hover_color="#4a9e4a",
                                        font=("SF Pro Display", 13, "bold"),
                                        command=lambda: self._complete_from_detail(dialog, task_id, team_id, team_name),
                                        corner_radius=10)
            btn_complete.pack(side="left", padx=(0, 10))

        if is_creator:
            btn_edit = ctk.CTkButton(left_btns, text="✎ Düzenle",
                                    width=120, height=40,
                                    fg_color=COLORS['accent_primary'],
                                    hover_color="#3a8eef",
                                    font=("SF Pro Display", 13, "bold"),
                                    command=lambda: self._edit_from_detail(dialog, task_id, team_id, team_name, members),
                                    corner_radius=10)
            btn_edit.pack(side="left", padx=(0, 10))

            btn_delete = ctk.CTkButton(left_btns, text="× Sil",
                                      width=120, height=40,
                                      fg_color=COLORS['accent_danger'],
                                      hover_color="#c8433d",
                                      font=("SF Pro Display", 13, "bold"),
                                      command=lambda: self._delete_from_detail(dialog, task_id, team_id, team_name),
                                      corner_radius=10)
            btn_delete.pack(side="left")

        # Sağ taraf: Kapat
        btn_close = ctk.CTkButton(btn_frame, text="Kapat",
                                  width=100, height=40,
                                  fg_color="transparent",
                                  hover_color=COLORS['hover'],
                                  border_width=1,
                                  border_color=COLORS['border'],
                                  font=("SF Pro Display", 13),
                                  command=dialog.destroy,
                                  corner_radius=10)
        btn_close.pack(side="right")

        # Eğer edit_mode True ise direkt düzenleme moduna geç
        if edit_mode and is_creator:
            dialog.destroy()
            self.edit_task_action(task_id, team_id, team_name, members)

    def _complete_from_detail(self, dialog, task_id, team_id, team_name):
        """Detay penceresinden tamamlama"""
        dialog.destroy()
        self.complete_task_action(task_id, team_id, team_name)

    def _edit_from_detail(self, dialog, task_id, team_id, team_name, members):
        """Detay penceresinden düzenleme"""
        dialog.destroy()
        self.edit_task_action(task_id, team_id, team_name, members)

    def _delete_from_detail(self, dialog, task_id, team_id, team_name):
        """Detay penceresinden silme"""
        dialog.destroy()
        self.delete_task_action(task_id, team_id, team_name)

    def edit_task_action(self, task_id, team_id, team_name, members):
        """Görev düzenleme dialog penceresi açar"""
        # Görev bilgilerini getir
        task = self.db.get_task_by_id(task_id)
        if not task:
            messagebox.showerror("Görev Bulunamadı",
                                "Seçilen görev bulunamadı.\n\nGörev silinmiş veya erişim yetkiniz olmayabilir.")
            return

        # task: (id, title, description, status, deadline, assigned_user_ids, assigned_user_names, created_by_id, created_by_username, created_at, team_id)
        task_title = task[1]
        task_desc = task[2]
        task_status = task[3]
        task_deadline = task[4]
        task_assigned_ids = task[5] if task[5] else []
        task_created_by = task[7]

        # Yetki kontrolü - sadece görevi oluşturan kişi düzenleyebilir
        if task_created_by != self.current_user_id:
            messagebox.showerror("Yetki Hatası",
                                "Bu görevi düzenleme yetkiniz yok.\n\nSadece görevi oluşturan kişi düzenleme yapabilir.")
            return

        # Dialog penceresi oluştur
        dialog = ctk.CTkToplevel(self)
        dialog.title("Görev Düzenle")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        # Başlık
        ctk.CTkLabel(dialog, text="Görev Düzenle", font=("Arial", 18, "bold")).pack(pady=20)

        # Form alanları
        form_frame = ctk.CTkScrollableFrame(dialog, fg_color="transparent")
        form_frame.pack(padx=20, pady=10, fill="both", expand=True)

        # Başlık
        ctk.CTkLabel(form_frame, text="Görev Başlığı",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_title = ctk.CTkEntry(form_frame, width=540, height=48,
                                   corner_radius=12, border_width=1,
                                   border_color=COLORS['border'],
                                   font=("SF Pro Display", 14))
        entry_title.insert(0, task_title)
        entry_title.pack(fill="x", pady=(0, 20))

        # Açıklama
        ctk.CTkLabel(form_frame, text="Açıklama",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_desc = ctk.CTkTextbox(form_frame, width=540, height=120,
                                   corner_radius=12, border_width=1,
                                   border_color=COLORS['border'],
                                   font=("SF Pro Display", 13))
        entry_desc.insert("1.0", task_desc if task_desc else "")
        entry_desc.pack(fill="x", pady=(0, 20))

        # Tarih
        ctk.CTkLabel(form_frame, text="Son Tarih (YYYY-MM-DD)",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        entry_deadline = ctk.CTkEntry(form_frame, width=540, height=48,
                                     corner_radius=12, border_width=1,
                                     border_color=COLORS['border'],
                                     font=("SF Pro Display", 14))
        entry_deadline.insert(0, str(task_deadline) if task_deadline else "")
        entry_deadline.pack(fill="x", pady=(0, 20))

        # Atanan kişiler (CheckBox listesi)
        ctk.CTkLabel(form_frame, text="Atanan Kişiler",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 12))
        edit_checkboxes = {}
        checkbox_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        checkbox_frame.pack(fill="x", pady=(0, 20))

        for member_id, member_name, role in members:
            var = ctk.BooleanVar(value=member_id in task_assigned_ids)
            cb = ctk.CTkCheckBox(checkbox_frame, text=member_name,
                               variable=var,
                               font=("SF Pro Display", 13),
                               corner_radius=6)
            cb.pack(side="left", padx=(0, 20))
            edit_checkboxes[member_id] = var

        # Durum
        ctk.CTkLabel(form_frame, text="Durum",
                    font=("SF Pro Display", 12, "bold"),
                    text_color=COLORS['text_secondary'],
                    anchor="w").pack(fill="x", pady=(0, 8))
        combo_status = ctk.CTkComboBox(form_frame, values=["Todo", "In Progress", "Done"],
                                      width=540, height=48,
                                      corner_radius=12, border_width=1,
                                      border_color=COLORS['border'],
                                      font=("SF Pro Display", 14),
                                      dropdown_font=("SF Pro Display", 14))
        combo_status.set(task_status)
        combo_status.pack(fill="x", pady=(0, 20))

        # Butonlar
        btn_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        btn_frame.pack(pady=20)

        def save_task():
            new_title = entry_title.get()
            new_desc = entry_desc.get("1.0", "end-1c")
            new_deadline = entry_deadline.get()
            new_status = combo_status.get()

            if not new_title or not new_deadline:
                messagebox.showwarning("Eksik Bilgi",
                                       "Lütfen tüm zorunlu alanları doldurun.\n\nGörev başlığı ve son tarih gereklidir.")
                return

            # Seçili CheckBox'ları bul
            assigned_ids = []
            assigned_names = []
            for member_id, var in edit_checkboxes.items():
                if var.get():
                    assigned_ids.append(member_id)
                    # İsim bul
                    for m in members:
                        if m[0] == member_id:
                            assigned_names.append(m[1])
                            break

            if not assigned_ids:
                messagebox.showwarning("Eksik Bilgi",
                                       "Lütfen en az bir kişi seçin.\n\nGörevi atamak için en az bir kişi seçmelisiniz.")
                return

            self.db.update_task(task_id, new_title, new_desc, assigned_ids, new_deadline, new_status)
            assigned_text = ", ".join(assigned_names)
            messagebox.showinfo("Görev Güncellendi",
                               f"Görev başarıyla güncellendi.\n\nBaşlık: {new_title}\nDurum: {new_status}\nAtanan: {assigned_text}")
            dialog.destroy()
            # team_name'i instance variable'dan al
            if hasattr(self, 'current_team_name'):
                self.show_team_page(team_id, self.current_team_name)
            else:
                self.show_team_page(team_id, team_name)

        ctk.CTkButton(btn_frame, text="Kaydet",
                     command=save_task,
                     fg_color=COLORS['accent_secondary'],
                     hover_color="#4a9e4a",
                     width=140, height=44,
                     corner_radius=10,
                     font=("SF Pro Display", 14, "bold")).pack(side="left", padx=(0, 10))
        ctk.CTkButton(btn_frame, text="İptal",
                     command=dialog.destroy,
                     fg_color="transparent",
                     hover_color=COLORS['hover'],
                     border_width=1,
                     border_color=COLORS['border'],
                     width=140, height=44,
                     corner_radius=10,
                     font=("SF Pro Display", 14)).pack(side="left")

if __name__ == "__main__":
    try:
        print("🚀 Uygulama başlatılıyor...")
        app = MainApp()
        print("✅ Uygulama başlatıldı!")
        app.mainloop()
    except Exception as e:
        import traceback
        print(f"❌ Kritik Hata: {e}")
        print("\n📋 Detaylı Hata Bilgisi:")
        traceback.print_exc()
        try:
            from tkinter import messagebox
            messagebox.showerror("Kritik Hata", f"Uygulama başlatılamadı:\n\n{e}\n\nDetaylar için terminal çıktısına bakın.")
        except:
            pass
        input("\nDevam etmek için Enter'a basın...")