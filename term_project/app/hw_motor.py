import RPi.GPIO as GPIO

class MotorController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(MotorController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
        
        self.MOTOR_P = 19
        self.MOTOR_M = 13
        
        # 모드 설정
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        GPIO.setup(self.MOTOR_M, GPIO.OUT)
        GPIO.setup(self.MOTOR_P, GPIO.OUT)
        
        # 초기 상태 정지
        self.stop()
        self._initialized = True
        
    def play(self):
        """음악 재생 시 모터 회전"""
        GPIO.output(self.MOTOR_M, GPIO.HIGH)
        GPIO.output(self.MOTOR_P, GPIO.LOW)
        
    def stop(self):
        """음악 정지 시 모터 정지"""
        GPIO.output(self.MOTOR_M, GPIO.LOW)
        GPIO.output(self.MOTOR_P, GPIO.LOW)
