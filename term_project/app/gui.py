import os
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QSlider
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QFont

class MusicPlayerGUI(QWidget):
    # 하드웨어 쓰레드에서 발생하는 이벤트를 GUI 스레드로 안전하게 전달하기 위한 PyQt 시그널
    sig_toggle_play = pyqtSignal()
    sig_next = pyqtSignal()
    sig_prev = pyqtSignal()
    sig_shuffle = pyqtSignal()
    sig_volume = pyqtSignal(int)
    
    def __init__(self, player):
        super().__init__()
        self.player = player
        self.initUI()
        
        # 하드웨어 이벤트 시그널을 GUI 컴포넌트 동작으로 연결
        self.sig_toggle_play.connect(self._on_toggle_play)
        self.sig_next.connect(self._on_next)
        self.sig_prev.connect(self._on_prev)
        self.sig_shuffle.connect(self._on_shuffle)
        self.sig_volume.connect(self._on_volume)
        
        # 곡 진행 시간 등을 주기적으로 갱신하기 위한 타이머
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_ui)
        self.timer.start(500)
        
    def initUI(self):
        self.setWindowTitle('Raspberry Pi Music Player')
        self.resize(450, 250)
        # 모던하고 어두운 테마 적용
        self.setStyleSheet("background-color: #2b2b2b; color: #ffffff;")
        
        layout = QVBoxLayout()
        layout.setContentsMargins(30, 30, 30, 30)
        layout.setSpacing(20)
        
        # 곡 타이틀 라벨
        self.lbl_title = QLabel('No Music', self)
        self.lbl_title.setAlignment(Qt.AlignCenter)
        self.lbl_title.setFont(QFont("Arial", 18, QFont.Bold))
        layout.addWidget(self.lbl_title)
        
        # 재생 진행 시간 라벨
        self.lbl_time = QLabel('00:00', self)
        self.lbl_time.setAlignment(Qt.AlignCenter)
        self.lbl_time.setFont(QFont("Arial", 12))
        layout.addWidget(self.lbl_time)
        
        # 볼륨 슬라이더 컨트롤
        vol_layout = QHBoxLayout()
        self.lbl_vol = QLabel('Vol', self)
        self.lbl_vol.setFont(QFont("Arial", 10))
        self.slider_vol = QSlider(Qt.Horizontal, self)
        self.slider_vol.setRange(0, 100)
        self.slider_vol.setValue(50)
        self.slider_vol.valueChanged.connect(self._on_gui_volume_change)
        
        vol_layout.addWidget(self.lbl_vol)
        vol_layout.addWidget(self.slider_vol)
        layout.addLayout(vol_layout)
        
        # 재생 컨트롤 버튼들
        btn_layout = QHBoxLayout()
        btn_style = """
            QPushButton {
                background-color: #4a4a4a;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """
        
        self.btn_prev = QPushButton('Prev', self)
        self.btn_play = QPushButton('Play/Pause', self)
        self.btn_next = QPushButton('Next', self)
        self.btn_shuffle = QPushButton('Shuffle', self)
        
        for btn in [self.btn_prev, self.btn_play, self.btn_next, self.btn_shuffle]:
            btn.setStyleSheet(btn_style)
            btn_layout.addWidget(btn)
            
        self.btn_prev.clicked.connect(self._on_prev)
        self.btn_play.clicked.connect(self._on_toggle_play)
        self.btn_next.clicked.connect(self._on_next)
        self.btn_shuffle.clicked.connect(self._on_shuffle)
        
        layout.addLayout(btn_layout)
        self.setLayout(layout)
        self.update_ui()
        
    def _on_toggle_play(self):
        self.player.toggle_play()
        self.update_ui()
        
    def _on_next(self):
        self.player.next_song()
        self.update_ui()
        
    def _on_prev(self):
        self.player.prev_song()
        self.update_ui()
        
    def _on_shuffle(self):
        self.player.shuffle()
        self.update_ui()
        
    def _on_volume(self, val):
        # 하드웨어에서 변경된 볼륨값을 슬라이더에 반영
        self.slider_vol.blockSignals(True)
        self.slider_vol.setValue(val)
        self.slider_vol.blockSignals(False)
        self.player.set_volume(val)
        
    def _on_gui_volume_change(self, val):
        # GUI에서 변경된 볼륨값을 오디오 시스템에 반영
        self.player.set_volume(val)
        
    def update_ui(self):
        """타이머에 의해 주기적으로 호출되어 화면을 갱신"""
        title = self.player.get_current_song_name()
        if not title:
            title = "No Music"
        self.lbl_title.setText(title)
        
        secs = int(self.player.get_progress())
        mins = secs // 60
        secs = secs % 60
        self.lbl_time.setText(f"{mins:02d}:{secs:02d}")
