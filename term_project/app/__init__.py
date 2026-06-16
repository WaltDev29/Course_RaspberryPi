import tkinter as tk
import queue

from .hw_motor import MotorController
from .hw_switch import SwitchController
from .hw_led import LEDController
from .hw_lcd import LCDController
from .hw_vr import VRController
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
    player = MusicPlayer()
    
    # GUI 인스턴스 생성 및 플레이어 주입
    gui = MusicPlayerGUI(root, player)
    
    # 3. 하드웨어 스위치 입력 처리 (tkinter 스레드 충돌 방지를 위해 Queue 사용)
    event_queue = queue.Queue()
    
    switch.register_callback(switch.SW1_PIN, lambda: event_queue.put('toggle'))
    switch.register_callback(switch.SW2_PIN, lambda: event_queue.put('prev'))
    switch.register_callback(switch.SW3_PIN, lambda: event_queue.put('next'))
    switch.register_callback(switch.SW4_PIN, lambda: event_queue.put('shuffle'))
    
    # 4. GUI 타이머 루프에 하드웨어 출력 상태 동기화 및 큐 처리 로직 주입(Hook)
    original_refresh_ui_state = gui.refresh_ui_state
    last_vr_volume = vr.volume
    
    def hooked_refresh_ui_state():
        nonlocal last_vr_volume
        # 4-1. 큐에 쌓인 스위치 인터럽트 이벤트 메인 스레드에서 처리
        while not event_queue.empty():
            action = event_queue.get()
            if action == 'toggle':
                gui._on_toggle_play()
            elif action == 'prev':
                gui._on_prev()
            elif action == 'next':
                gui._on_next()
            elif action == 'shuffle':
                gui._on_shuffle()
                
        # 4-2. VR 볼륨에 변화가 있을 때만 GUI 슬라이더 동기화
        if vr.volume != last_vr_volume:
            gui.slider_vol.set(vr.volume)
            last_vr_volume = vr.volume
        
        # 4-3. GUI 텍스트 및 프로그레스 갱신 (기존 함수)
        original_refresh_ui_state()
        
        # 4-4. 출력 하드웨어(LED, LCD, Motor) 상태 플레이어와 동기화
        is_playing = player.is_playing
        led.set_playing(is_playing)
        lcd.set_playing(is_playing)
        lcd.set_title(player.get_current_song_name() if is_playing else "")
        
        if is_playing:
            motor.play()
        else:
            motor.stop()
            
    # 후킹된 함수로 교체
    gui.refresh_ui_state = hooked_refresh_ui_state
    
    return root, gui
