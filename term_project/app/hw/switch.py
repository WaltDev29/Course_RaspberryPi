import RPi.GPIO as GPIO

class SwitchController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(SwitchController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.SW1_PIN = 4
        self.SW2_PIN = 17
        self.SW3_PIN = 18
        self.SW4_PIN = 22
        self.SW_PIN_LIST = [self.SW1_PIN, self.SW2_PIN, self.SW3_PIN, self.SW4_PIN]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.SW_PIN_LIST, GPIO.IN)
        
        self.callbacks = {
            self.SW1_PIN: None,
            self.SW2_PIN: None,
            self.SW3_PIN: None,
            self.SW4_PIN: None
        }
        self._initialized = True
        
    def register_callback(self, pin, callback):
        """특정 핀에 콜백 등록 (비동기 인터럽트 활용)"""
        self.callbacks[pin] = callback
        
        # 기존에 등록된 이벤트가 있다면 삭제 (중복 방지)
        try:
            GPIO.remove_event_detect(pin)
        except RuntimeError:
            pass
            
        # 스위치가 눌리면 보통 LOW로 떨어지므로 FALLING 엣지 감지 (바운싱 방지 300ms)
        GPIO.add_event_detect(pin, GPIO.FALLING, callback=self._btn_callback, bouncetime=300)
        
    def _btn_callback(self, channel):
        """등록된 콜백 함수 실행"""
        if self.callbacks.get(channel):
            self.callbacks[channel]()
