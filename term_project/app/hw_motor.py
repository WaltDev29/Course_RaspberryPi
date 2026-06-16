import RPi.GPIO as GPIO
import threading
import time

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
            
        self.STEP_IN1 = 16
        self.STEP_IN2 = 20
        self.STEP_IN3 = 21
        self.STEP_IN4 = 26
        self.pinsArray = [self.STEP_IN1, self.STEP_IN2, self.STEP_IN3, self.STEP_IN4]
        
        # 1상 여자방식 신호 (풀 스텝)
        self.signal_full = [
            [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
            [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
            [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
            [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
        ]
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        for pin in self.pinsArray:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, GPIO.LOW)
            
        self.is_playing = False
        
        # 스텝 모터는 지속적인 신호(펄스)를 줘야 회전하므로 별도 스레드 운영
        self.thread = threading.Thread(target=self._motor_loop, daemon=True)
        self.thread.start()
        
        self._initialized = True
        
    def play(self):
        """음악 재생 시 모터 회전 상태로 변경"""
        self.is_playing = True
        
    def stop(self):
        """음악 정지 시 모터 회전 상태 해제 및 핀 초기화"""
        self.is_playing = False
        for pin in self.pinsArray:
            GPIO.output(pin, GPIO.LOW)
            
    def _motor_loop(self):
        """백그라운드 스텝 모터 회전 루프"""
        while True:
            if self.is_playing:
                # 4단계 신호를 차례대로 인가
                for step_idx in range(4):
                    if not self.is_playing: # 회전 도중 중지 신호 발생 시 루프 즉시 이탈
                        break
                    for idx in range(4):
                        GPIO.output(self.pinsArray[idx], self.signal_full[step_idx][idx])
                    time.sleep(0.002) # 예제에 따른 스텝 간격
            else:
                # 회전하지 않을 때는 CPU 점유를 낮추기 위해 긴 대기
                time.sleep(0.1)
