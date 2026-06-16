import RPi.GPIO as GPIO
import threading
import time

class KeypadController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(KeypadController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.COL_LIST = [5, 6, 7]
        self.ROW_LIST = [8, 9, 10, 11]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        try:
            GPIO.setup(self.COL_LIST, GPIO.OUT)
            GPIO.setup(self.ROW_LIST, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            for col in self.COL_LIST:
                GPIO.output(col, GPIO.LOW)
        except Exception as e:
            print(f"Keypad GPIO 초기화 실패: {e}")
            
        self.on_press = None
        self.on_release = None
        
        self.is_running = True
        self.thread = threading.Thread(target=self._poll_loop, daemon=True)
        self.thread.start()
        
        self._initialized = True
        
    def register_callback(self, on_press, on_release):
        """버튼을 눌렀을 때와 뗐을 때 실행할 콜백 함수 등록"""
        self.on_press = on_press
        self.on_release = on_release
        
    def _set_col_out(self, col_idx):
        for enable_idx in range(3):
            if col_idx == enable_idx:
                GPIO.output(self.COL_LIST[enable_idx], GPIO.HIGH)
            else:
                GPIO.output(self.COL_LIST[enable_idx], GPIO.LOW)
                
    def _get_keypad(self):
        result = -1
        for col in range(3):
            self._set_col_out(col)
            for row in range(4):
                if GPIO.input(self.ROW_LIST[row]) == GPIO.HIGH:
                    # 1부터 12까지의 숫자
                    result = (row * 3) + col + 1
        return result
        
    def _poll_loop(self):
        """백그라운드에서 주기적으로 키패드 상태를 읽어 이벤트 발생"""
        last_key = -1
        while self.is_running:
            try:
                current_key = self._get_keypad()
                if current_key != last_key:
                    # 이전 키 해제 이벤트
                    if last_key != -1 and self.on_release:
                        self.on_release(last_key)
                    # 새 키 누름 이벤트
                    if current_key != -1 and self.on_press:
                        self.on_press(current_key)
                    last_key = current_key
            except Exception:
                pass
            time.sleep(0.05) # 50ms 주기로 스캔
            
    def cleanup(self):
        self.is_running = False
        try:
            for col in self.COL_LIST:
                GPIO.output(col, GPIO.LOW)
        except:
            pass
