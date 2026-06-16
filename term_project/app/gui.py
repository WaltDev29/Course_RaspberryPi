import tkinter as tk
from tkinter import ttk

class MusicPlayerGUI:
    def __init__(self, root, player):
        self.root = root
        self.player = player
        
        self.initUI()
        
        # 주기적 UI 갱신 (500ms 단위)
        self.update_ui()
        
    def initUI(self):
        self.root.title('Raspberry Pi Music Player')
        self.root.geometry('450x250')
        self.root.configure(bg='#2b2b2b')
        
        style = ttk.Style()
        # 기본 테마보다 모던한 clam 테마가 있으면 사용
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('TButton', background='#4a4a4a', foreground='#ffffff', font=('Arial', 10, 'bold'), padding=5)
        style.map('TButton', background=[('active', '#5a5a5a')])
        
        # 타이틀
        self.lbl_title = ttk.Label(self.root, text='No Music', font=('Arial', 18, 'bold'))
        self.lbl_title.pack(pady=20)
        
        # 시간 표시
        self.lbl_time = ttk.Label(self.root, text='00:00', font=('Arial', 12))
        self.lbl_time.pack()
        
        # 볼륨 조절부
        vol_frame = tk.Frame(self.root, bg='#2b2b2b')
        vol_frame.pack(pady=10)
        
        ttk.Label(vol_frame, text='Vol').pack(side=tk.LEFT, padx=5)
        
        self.slider_vol = ttk.Scale(vol_frame, from_=0, to=100, orient=tk.HORIZONTAL, length=200, command=self._on_gui_volume_change)
        self.slider_vol.set(50)
        self.slider_vol.pack(side=tk.LEFT)
        
        # 컨트롤 버튼부
        btn_frame = tk.Frame(self.root, bg='#2b2b2b')
        btn_frame.pack(pady=20)
        
        self.btn_prev = ttk.Button(btn_frame, text='Prev', command=self._on_prev)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        
        self.btn_play = ttk.Button(btn_frame, text='Play/Pause', command=self._on_toggle_play)
        self.btn_play.pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(btn_frame, text='Next', command=self._on_next)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_shuffle = ttk.Button(btn_frame, text='Shuffle', command=self._on_shuffle)
        self.btn_shuffle.pack(side=tk.LEFT, padx=5)
        
    def _on_toggle_play(self):
        self.player.toggle_play()
        self.refresh_ui_state()
        
    def _on_next(self):
        self.player.next_song()
        self.refresh_ui_state()
        
    def _on_prev(self):
        self.player.prev_song()
        self.refresh_ui_state()
        
    def _on_shuffle(self):
        self.player.shuffle()
        self.refresh_ui_state()
        
    def _on_gui_volume_change(self, val):
        self.player.set_volume(float(val))
        
    def refresh_ui_state(self):
        """UI 컴포넌트들의 상태를 현재 플레이어 상태에 맞게 갱신"""
        title = self.player.get_current_song_name()
        if not title:
            title = "No Music"
        self.lbl_title.config(text=title)
        
        secs = int(self.player.get_progress())
        mins = secs // 60
        secs = secs % 60
        self.lbl_time.config(text=f"{mins:02d}:{secs:02d}")
        
    def update_ui(self):
        """0.5초마다 주기적으로 UI 갱신 (tkinter의 after 함수 이용)"""
        self.refresh_ui_state()
        self.root.after(500, self.update_ui)
