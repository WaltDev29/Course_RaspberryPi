import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from .gui_keypad import VirtualKeypadWindow

class MusicPlayerGUI:
    def __init__(self, root, player):
        self.root = root
        self.player = player
        
        self.after_id = None
        self.initUI()
        
        # 주기적 UI 갱신 (500ms 단위)
        self.update_ui()
        
    def initUI(self):
        self.root.title('Raspberry Pi Music Player')
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.geometry('450x250')
        self.root.configure(bg='#2b2b2b')
        
        style = ttk.Style()
        # 기본 테마보다 모던한 clam 테마가 있으면 사용
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure('TLabel', background='#2b2b2b', foreground='#ffffff')
        style.configure('TButton', background='#4a4a4a', foreground='#ffffff', font=('Arial', 12, 'bold'), padding=5)
        style.map('TButton', background=[('active', '#5a5a5a')])
        
        # 전체 레이아웃 구성을 위한 프레임 분리
        main_frame = tk.Frame(self.root, bg='#2b2b2b')
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 좌측: 곡 정보 및 컨트롤
        left_frame = tk.Frame(main_frame, bg='#2b2b2b')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 우측: 세로형 볼륨 슬라이더
        vol_frame = tk.Frame(main_frame, bg='#2b2b2b')
        vol_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=20, pady=20)
        
        # --- 좌측 최상단 파일 선택 영역 ---
        top_frame = tk.Frame(left_frame, bg='#2b2b2b')
        top_frame.pack(fill=tk.X, pady=5, padx=10)
        self.btn_open = ttk.Button(top_frame, text='Open File', command=self._on_open_file)
        self.btn_open.pack(side=tk.LEFT)
        
        # --- 좌측 곡 정보 영역 ---
        self.lbl_title = ttk.Label(left_frame, text='No Music', font=('Arial', 18, 'bold'))
        self.lbl_title.pack(pady=15)
        
        self.lbl_time = ttk.Label(left_frame, text='00:00', font=('Arial', 12))
        self.lbl_time.pack()
        
        # --- 좌측 컨트롤 버튼 영역 ---
        btn_frame = tk.Frame(left_frame, bg='#2b2b2b')
        btn_frame.pack(pady=20)
        
        self.btn_prev = ttk.Button(btn_frame, text='<', command=self._on_prev, width=3)
        self.btn_prev.pack(side=tk.LEFT, padx=5)
        
        self.btn_play = ttk.Button(btn_frame, text='▷', command=self._on_toggle_play, width=4)
        self.btn_play.pack(side=tk.LEFT, padx=5)
        
        self.btn_next = ttk.Button(btn_frame, text='>', command=self._on_next, width=3)
        self.btn_next.pack(side=tk.LEFT, padx=5)
        
        self.btn_shuffle = ttk.Button(btn_frame, text='Shuffle', command=self._on_shuffle)
        self.btn_shuffle.pack(side=tk.LEFT, padx=5)
        
        # --- 우측 세로 볼륨 영역 ---
        self.btn_keypad = ttk.Button(vol_frame, text='Keypad', command=self._open_keypad_window, width=7)
        self.btn_keypad.pack(side=tk.TOP, pady=(0, 15))
        ttk.Label(vol_frame, text='Vol', font=('Arial', 10)).pack(side=tk.TOP, pady=5)
        # 세로 슬라이더는 from_=100, to=0으로 해야 위로 올릴수록 볼륨이 커짐
        self.slider_vol = ttk.Scale(vol_frame, from_=100, to=0, orient=tk.VERTICAL, length=140, command=self._on_gui_volume_change)
        self.slider_vol.set(0)
        self.slider_vol.pack(side=tk.TOP)
        
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
        
    def _on_open_file(self):
        filepath = filedialog.askopenfilename(
            title="Select Music File",
            filetypes=[("Audio Files", "*.mp3 *.wav"), ("All Files", "*.*")]
        )
        if filepath:
            self.player.add_and_play(filepath)
            self.refresh_ui_state()
        
    def _open_keypad_window(self):
        # 이미 창이 열려있는지 확인 (싱글톤 창)
        if hasattr(self, 'keypad_app') and self.keypad_app is not None and self.keypad_app.window.winfo_exists():
            self.keypad_app.window.lift() # 이미 열려있으면 최상단으로 끌어올림
            return
            
        # 별도 파일로 분리된 VirtualKeypadWindow 클래스 인스턴스화
        self.keypad_app = VirtualKeypadWindow(self.root)

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
        
        # 재생 상태에 따라 버튼 텍스트(아이콘) 동적 변경
        if self.player.is_playing:
            self.btn_play.config(text='||')
        else:
            self.btn_play.config(text='▷')
        
    def update_ui(self):
        """0.5초마다 주기적으로 UI 갱신 (tkinter의 after 함수 이용)"""
        try:
            self.refresh_ui_state()
            self.after_id = self.root.after(500, self.update_ui)
        except tk.TclError:
            pass
            
    def on_closing(self):
        """창을 닫을 때 예약된 타이머를 안전하게 취소하고 창을 파괴합니다."""
        if self.after_id:
            try:
                self.root.after_cancel(self.after_id)
            except Exception:
                pass
        self.root.destroy()
