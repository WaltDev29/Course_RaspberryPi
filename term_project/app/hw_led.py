import smbus
import threading
import time

class LEDController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LEDController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.bus = smbus.SMBus(1)
        self.addr = 0x20
        self.RED = 0b00000001
        self.GREEN = 0b00000010
        self.BLUE = 0b00000100
        self.colors = [self.RED, self.GREEN, self.BLUE]
        
        self.is_playing = False
        
        # 초기화 시 LED 전부 소등
        self.bus.write_byte(self.addr, 0)
        
        # 백그라운드 스레드로 LED 점멸 로직 실행
        self.thread = threading.Thread(target=self._led_loop, daemon=True)
        self.thread.start()
        self._initialized = True
        
    def set_playing(self, playing):
        """음악 재생 여부 상태 업데이트"""
        self.is_playing = playing
        if not playing:
            # 정지 시 LED 소등
            self.bus.write_byte(self.addr, 0)
            
    def cleanup(self):
        self.set_playing(False)
            
    def _led_loop(self):
        """백그라운드에서 동작하는 LED 순차 점멸 루프"""
        color_idx = 0
        while True:
            if self.is_playing:
                self.bus.write_byte(self.addr, self.colors[color_idx])
                color_idx = (color_idx + 1) % 3
            time.sleep(0.5) # 요구사항에 따라 순차 깜빡임 간격 0.5초 설정
