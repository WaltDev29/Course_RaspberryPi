import sys
from PyQt5.QtWidgets import QApplication

# 각 하드웨어 및 로직 모듈 임포트
from .hw_motor import MotorController
from .hw_switch import SwitchController
from .hw_led import LEDController
from .hw_lcd import LCDController
from .hw_vr import VRController
from .player import MusicPlayer
from .gui import MusicPlayerGUI

def create_app():
    """모든 모듈을 초기화하고 이벤트를 바인딩한 후 애플리케이션 객체를 반환합니다."""
    
    # 1. PyQt Application 객체 확보
    app = QApplication.instance()
    if app is None:
        app = QApplication(sys.argv)
        
    # 2. 싱글톤 객체들 초기화 (최초 1회 생성됨)
    motor = MotorController()
    switch = SwitchController()
    led = LEDController()
    lcd = LCDController()
    vr = VRController()
    player = MusicPlayer()
    
    # GUI 인스턴스 생성 및 플레이어 주입
    gui = MusicPlayerGUI(player)
    
    # 3. 하드웨어 입력(스위치, 가변저항)을 GUI 시그널에 바인딩
    # 스레드 충돌을 피하기 위해 센서 콜백에서는 GUI의 pyqtSignal.emit()만 호출함
    switch.register_callback(switch.SW1_PIN, lambda: gui.sig_toggle_play.emit())
    switch.register_callback(switch.SW2_PIN, lambda: gui.sig_prev.emit())
    switch.register_callback(switch.SW3_PIN, lambda: gui.sig_next.emit())
    switch.register_callback(switch.SW4_PIN, lambda: gui.sig_shuffle.emit())
    
    vr.register_callback(lambda vol: gui.sig_volume.emit(vol))
    
    # 4. GUI 타이머 루프에 하드웨어 출력 상태 동기화 로직 주입(Hook)
    # 0.5초마다 GUI가 갱신될 때 모터, LED, LCD의 상태도 현재 플레이어 상태에 맞춰 갱신됨
    original_update_ui = gui.update_ui
    
    def hooked_update_ui():
        original_update_ui() # 기존 GUI 업데이트 (라벨, 시간 갱신)
        
        is_playing = player.is_playing
        
        # LED, LCD 상태 전달
        led.set_playing(is_playing)
        lcd.set_playing(is_playing)
        
        # 타이틀이 재생 중일 때만 스크롤되도록 전달, 정지 시에는 빈 문자열 전달됨
        lcd.set_title(player.get_current_song_name() if is_playing else "")
        
        # 모터 제어
        if is_playing:
            motor.play()
        else:
            motor.stop()
            
    # 후킹된 함수로 교체
    gui.update_ui = hooked_update_ui
    
    return app, gui
