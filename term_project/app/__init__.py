import tkinter as tk

from .hw.motor import MotorController
from .hw.switch import SwitchController
from .hw.led import LEDController
from .hw.lcd import LCDController
from .hw.vr import VRController
from .hw.keypad import KeypadController
from .player import MusicPlayer
from .gui import MusicPlayerGUI

def create_app():
    """모든 모듈을 초기화하고 이벤트를 바인딩한 후 메인 윈도우 객체를 반환합니다."""
    
    # 1. tkinter Root 객체 생성
    root = tk.Tk()
        
    # 2. 싱글톤 객체들 초기화
    motor = MotorController()
    switch = SwitchController()
    led = LEDController()
    lcd = LCDController()
    vr = VRController()
    keypad = KeypadController()
    player = MusicPlayer()
    
    # GUI 인스턴스 생성 및 플레이어 주입
    gui = MusicPlayerGUI(root, player)
    
    # 3. 하드웨어 스위치/키패드 이벤트 바인딩 (Queue 대신 root.after를 이용해 즉각적인 스레드 안전 콜백 실행)
    switch.register_callback(switch.SW1_PIN, lambda: root.after(0, gui._on_toggle_play))
    switch.register_callback(switch.SW2_PIN, lambda: root.after(0, gui._on_prev))
    switch.register_callback(switch.SW3_PIN, lambda: root.after(0, gui._on_next))
    switch.register_callback(switch.SW4_PIN, lambda: root.after(0, gui._on_shuffle))
    
    def on_keypad_press(key):
        if hasattr(gui, 'keypad_app') and gui.keypad_app:
            root.after(0, gui.keypad_app.highlight_button, key)
            
    def on_keypad_release(key):
        if hasattr(gui, 'keypad_app') and gui.keypad_app:
            root.after(0, gui.keypad_app.unhighlight_button, key)
            
    keypad.register_callback(on_keypad_press, on_keypad_release)
    
    # 4. GUI 타이머 루프에 하드웨어 출력 상태 동기화 로직 주입(Hook)
    original_refresh_ui_state = gui.refresh_ui_state
    last_vr_volume = vr.volume
    
    def hooked_refresh_ui_state():
        nonlocal last_vr_volume
                
        # 4-1. VR 볼륨에 변화가 있을 때만 GUI 슬라이더 동기화
        if vr.volume != last_vr_volume:
            gui.slider_vol.set(vr.volume)
            last_vr_volume = vr.volume
        
        # 4-3. GUI 텍스트 및 프로그레스 갱신 (기존 함수)
        original_refresh_ui_state()
        
        # 4-4. 출력 하드웨어(LED, LCD, Motor) 상태 플레이어와 동기화
        is_playing = player.is_playing
        led.set_playing(is_playing)
        lcd.set_playing(is_playing)
        lcd.set_title(player.get_current_song_name())
        
        if is_playing:
            motor.play()
        else:
            motor.stop()
            
    # 후킹된 함수로 교체
    gui.refresh_ui_state = hooked_refresh_ui_state
    
    return root, gui

def cleanup_app():
    """종료 시 모든 싱글톤 객체들의 하드웨어/메모리 자원을 안전하게 해제합니다."""
    try:
        MotorController().cleanup()
    except: pass
    
    try:
        LEDController().cleanup()
    except: pass
    
    try:
        LCDController().cleanup()
    except: pass
    
    try:
        MusicPlayer().cleanup()
    except: pass
    
    try:
        KeypadController().cleanup()
    except: pass
