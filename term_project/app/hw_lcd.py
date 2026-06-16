import threading
import time
from . import RPi_I2C_driver # 상대 경로로 같은 폴더의 드라이버 임포트

class LCDController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(LCDController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.lcd = RPi_I2C_driver.lcd()
        self.lcd.lcd_clear()
        
        # 1번째 줄은 고정 출력
        self.lcd.lcd_display_string("now playing...", 1)
        
        self.is_playing = False
        self.title = ""
        
        # 텍스트 스크롤링을 위한 백그라운드 스레드
        self.thread = threading.Thread(target=self._scroll_loop, daemon=True)
        self.thread.start()
        self._initialized = True
        
    def set_title(self, title):
        """재생할 음악 제목 설정"""
        self.title = title
        if not title:
            # 제목이 없을 때 (정지 및 초기 상태) 2번째 줄 비우기
            self.lcd.lcd_display_string("                ", 2)
            
    def set_playing(self, playing):
        """재생 상태 설정"""
        self.is_playing = playing
        if not playing:
            # 정지 시 2번째 줄 초기화 (코멘트 요구사항 반영)
            self.lcd.lcd_display_string("                ", 2)
            
    def _scroll_loop(self):
        """백그라운드 스크롤 루프"""
        pos = 0
        while True:
            if self.is_playing and self.title:
                # 16칸 빈공간 + 타이틀 + 16칸 빈공간을 통해 스크롤 윈도우 구성
                display_text = "                " + self.title + "                "
                
                if pos > len(display_text) - 16:
                    pos = 0
                    
                chunk = display_text[pos:pos+16]
                self.lcd.lcd_display_string(chunk, 2)
                pos += 1
            time.sleep(0.3) # 스크롤 속도
