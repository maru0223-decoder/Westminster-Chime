import customtkinter as ctk
from PIL import Image, ImageOps, ImageSequence
import pygame
import threading
import time
from datetime import datetime
import os
import sys
from plyer import notification

class JamGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Westminster - All-in-One Edition")
        self.geometry("960x540")
        self.resizable(True, True)

        self.log_history = []
        self.log_window = None
        self.current_lang = "EN"
        self.lang_data = {
            "EN": {"log": "Log", "pinned": "Pinned", "full": "Full", "status_on": "Status: RUNNING", "status_off": "Status: STOPPED", "browse": "🎵 Browse Audio", "active": "Active Chime Hours:", "to": "to", "vol": "Volume Audio:", "btn_start": "Start Chime", "btn_stop": "Stop Chime"},
            "CN": {"log": "日志", "pinned": "置顶", "full": "全屏", "status_on": "状态: 运行中", "status_off": "状态: 已停止", "browse": "🎵 选择音频", "active": "钟声活跃时间:", "to": "至", "vol": "音频音量:", "btn_start": "开始运行", "btn_stop": "停止运行"},
            "JP": {"log": "ログ", "pinned": "ピン留め", "full": "全画面", "status_on": "状態: 実行中", "status_off": "状態: 停止中", "browse": "🎵 音声を選択", "active": "チャイム作動時間:", "to": "～", "vol": "音量:", "btn_start": "開始", "btn_stop": "停止"}
        }

        pygame.mixer.init()
        self.CHIMES = {0: "chime_00.wav", 15: "chime_15.wav", 30: "chime_30.wav", 45: "chime_45.wav"}
        self.is_running = False
        self.audio_folder = r"D:\TIME PY\chime collection\classic chime"
        
        self.bg_label = ctk.CTkLabel(self, text="")
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        self.gif_frames = []
        self.gif_index = 0
        self.muat_background()

        self.build_ui()
        self.update_digital_clock()
        self.catat_log("✨ Sistem Westminster dimuat.")

    def update_digital_clock(self):
        self.lbl_clock.configure(text=datetime.now().strftime("%H:%M:%S"))
        self.after(1000, self.update_digital_clock)

    def muat_background(self):
        gif_path = "anime_bg.gif"
        if os.path.exists(gif_path):
            try:
                gif_img = Image.open(gif_path)
                for frame in ImageSequence.Iterator(gif_img):
                    resized = frame.convert("RGBA")
                    self.gif_frames.append(ctk.CTkImage(resized, size=(960, 540)))
                self.animasi_gif()
            except: pass
        else:
            try:
                img = Image.open("anime_bg.png")
                self.bg_label.configure(image=ctk.CTkImage(img, size=(960, 540)))
            except: pass

    def animasi_gif(self):
        if self.gif_frames:
            self.bg_label.configure(image=self.gif_frames[self.gif_index])
            self.gif_index = (self.gif_index + 1) % len(self.gif_frames)
            self.after(40, self.animasi_gif)

    def tampilkan_notifikasi(self, judul, pesan):
        threading.Thread(target=lambda: notification.notify(title=judul, message=pesan, timeout=5), daemon=True).start()

    def catat_log(self, pesan):
        waktu = datetime.now().strftime('%H:%M:%S')
        teks_log = f"[{waktu}] {pesan}"
        self.log_history.append(teks_log)
        if self.log_window and self.log_window.winfo_exists():
            self.textbox_log.configure(state="normal")
            self.textbox_log.insert("end", teks_log + "\n")
            self.textbox_log.see("end")
            self.textbox_log.configure(state="disabled")
        if any(x in pesan for x in ["🔔", "🌙", "🚀"]): self.tampilkan_notifikasi("Notifikasi Jam", pesan)

    def buka_log(self):
        if self.log_window is None or not self.log_window.winfo_exists():
            self.log_window = ctk.CTkToplevel(self)
            self.log_window.title("Terminal Log")
            self.log_window.geometry("450x300")
            self.textbox_log = ctk.CTkTextbox(self.log_window, font=ctk.CTkFont("Consolas", 12), fg_color="#1E1E1E", text_color="#A6E22E")
            self.textbox_log.pack(pady=10, padx=10, fill="both", expand=True)
            self.textbox_log.configure(state="normal")
            for log in self.log_history: self.textbox_log.insert("end", log + "\n")
            self.textbox_log.configure(state="disabled")

    def change_lang(self, choice):
        self.current_lang = choice
        d = self.lang_data[choice]
        self.btn_log.configure(text=d["log"]); self.check_pinned.configure(text=d["pinned"])
        self.check_fullscreen.configure(text=d["full"]); self.lbl_active_time.configure(text=d["active"])
        self.lbl_to.configure(text=d["to"]); self.lbl_vol.configure(text=d["vol"])
        self.btn_toggle.configure(text=d["btn_start"] if not self.is_running else d["btn_stop"])

    def build_ui(self):
        warna_teks = "#5C4A3D"
        self.ghost_frame = ctk.CTkFrame(self, fg_color="#F0EAE1", bg_color="transparent", corner_radius=0, border_width=2, border_color="#D9C3A1")
        self.ghost_frame.place(relx=0.02, rely=0.03, relwidth=0.45, relheight=0.94)

        # Header
        frame_top = ctk.CTkFrame(self.ghost_frame, fg_color="transparent")
        frame_top.pack(fill="x", padx=10, pady=(10, 0))
        self.btn_log = ctk.CTkButton(frame_top, text="Log", width=60, height=25, font=("Century Gothic", 13), command=self.buka_log, fg_color="#FDFBF7", text_color=warna_teks, border_color="#D9C3A1", border_width=1)
        self.btn_log.pack(side="left")
        self.lang_menu = ctk.CTkOptionMenu(frame_top, values=["EN", "CN", "JP"], command=self.change_lang, width=60, fg_color="#CDB284")
        self.lang_menu.pack(side="left", padx=5)
        self.check_pinned = ctk.CTkCheckBox(frame_top, text="Pinned", text_color=warna_teks, font=("Century Gothic", 12, "bold"), command=lambda: self.attributes('-topmost', self.check_pinned.get()))
        self.check_pinned.pack(side="right", padx=5)
        self.check_fullscreen = ctk.CTkCheckBox(frame_top, text="Full", text_color=warna_teks, font=("Century Gothic", 12, "bold"), command=lambda: self.attributes('-fullscreen', self.check_fullscreen.get()))
        self.check_fullscreen.pack(side="right", padx=5)

        self.lbl_clock = ctk.CTkLabel(self.ghost_frame, text="00:00:00", font=("Consolas", 42, "bold"), text_color=warna_teks)
        self.lbl_clock.pack(pady=(10, 0))
        ctk.CTkLabel(self.ghost_frame, text="Westminster", font=("Georgia", 32, "bold", "italic"), text_color="#B28859").pack()
        self.lbl_status = ctk.CTkLabel(self.ghost_frame, text="Status: STOPPED", text_color="#BC655B", font=("Century Gothic", 12, "bold"))
        self.lbl_status.pack(pady=(0, 20))

        self.btn_folder = ctk.CTkButton(self.ghost_frame, text="🎵 Browse Audio", font=("Century Gothic", 14, "bold"), command=self.pilih_folder, fg_color="#CDB284", text_color="#4A3B32", corner_radius=20, height=35, width=180)
        self.btn_folder.pack(pady=5)
        self.lbl_folder_path = ctk.CTkLabel(self.ghost_frame, text=f".../{os.path.basename(self.audio_folder)}", font=("Century Gothic", 10), text_color="#9A8C7F")
        self.lbl_folder_path.pack(pady=(0, 15))

        self.lbl_active_time = ctk.CTkLabel(self.ghost_frame, text="Active Chime Hours:", font=("Century Gothic", 13), text_color=warna_teks)
        self.lbl_active_time.pack(pady=(5, 5))
        frame_jam = ctk.CTkFrame(self.ghost_frame, fg_color="transparent")
        frame_jam.pack(pady=5)
        entry_style = {"width": 45, "height": 35, "justify": "center", "font": ("Century Gothic", 18, "bold"), "fg_color": "#FFFFFF", "text_color": warna_teks, "border_color": "#D9C3A1", "border_width": 2, "corner_radius": 8}
        
        self.jam_mulai = ctk.CTkEntry(frame_jam, **entry_style); self.jam_mulai.insert(0, "04"); self.jam_mulai.pack(side="left")
        ctk.CTkLabel(frame_jam, text=":", font=("Century Gothic", 18, "bold"), text_color=warna_teks).pack(side="left", padx=2)
        self.menit_mulai = ctk.CTkEntry(frame_jam, **entry_style); self.menit_mulai.insert(0, "00"); self.menit_mulai.pack(side="left")
        self.lbl_to = ctk.CTkLabel(frame_jam, text="to", font=("Century Gothic", 13), text_color=warna_teks); self.lbl_to.pack(side="left", padx=10)
        self.jam_selesai = ctk.CTkEntry(frame_jam, **entry_style); self.jam_selesai.insert(0, "22"); self.jam_selesai.pack(side="left")
        ctk.CTkLabel(frame_jam, text=":", font=("Century Gothic", 18, "bold"), text_color=warna_teks).pack(side="left", padx=2)
        self.menit_selesai = ctk.CTkEntry(frame_jam, **entry_style); self.menit_selesai.insert(0, "00"); self.menit_selesai.pack(side="left")

        self.lbl_vol = ctk.CTkLabel(self.ghost_frame, text="Volume Audio:", font=("Century Gothic", 13), text_color=warna_teks)
        self.lbl_vol.pack(pady=(15, 5))
        self.slider_vol = ctk.CTkSlider(self.ghost_frame, from_=0, to=1, command=lambda v: pygame.mixer.music.set_volume(v), button_color="#CDB284", progress_color="#CDB284", height=12)
        self.slider_vol.set(0.6)
        self.slider_vol.pack(pady=5, padx=30)
        self.btn_toggle = ctk.CTkButton(self.ghost_frame, text="Start Chime", command=self.toggle_jam, height=40, width=160, font=("Century Gothic", 14, "bold"), fg_color="#7C9A82", text_color="#FFFFFF", corner_radius=20)
        self.btn_toggle.pack(pady=25)

    def pilih_folder(self): 
        f = ctk.filedialog.askdirectory(); 
        if f: self.audio_folder = f; self.lbl_folder_path.configure(text=f".../{os.path.basename(f)}")
    def toggle_jam(self):
        self.is_running = not self.is_running
        d = self.lang_data[self.current_lang]
        self.lbl_status.configure(text=d["status_on"] if self.is_running else d["status_off"])
        self.btn_toggle.configure(text=d["btn_start"] if not self.is_running else d["btn_stop"])
        if self.is_running: threading.Thread(target=self.clock_loop, daemon=True).start()
    def clock_loop(self):
        while self.is_running:
            now = datetime.now()
            if now.minute in self.CHIMES and now.second == 0:
                self.play_chime(now.minute)
                time.sleep(1)
            time.sleep(0.5)
    def play_chime(self, minute):
        path = os.path.join(self.audio_folder, self.CHIMES.get(minute))
        if os.path.exists(path):
            pygame.mixer.music.load(path); pygame.mixer.music.play(); self.catat_log(f"🔔 Memutar {self.CHIMES.get(minute)}")
        else: self.catat_log(f"⚠️ File tidak ditemukan")

if __name__ == "__main__":
    app = JamGUI()
    app.mainloop()