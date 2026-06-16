import smbus
import threading
import time

class VRController:
    _instance = None
    
    def __new__(cls):
        if not cls._instance:
            cls._instance = super(VRController, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance
        
    def __init__(self):
        if self._initialized:
            return
            
        self.bus = smbus.SMBus(1)
        self.i2c_address = 0x48
        self.command = 0x44
        
        self.volume = 0
        self.callback = None
        
        # I2C 데이터를 지속적으로 읽어오기 위한 데몬 스레드
        self.thread = threading.Thread(target=self._read_loop, daemon=True)
        self.thread.start()
        self._initialized = True
        
    def register_callback(self, callback):
        """볼륨이 변할 때 호출될 콜백 함수 등록"""
        self.callback = callback
        
    def _read_loop(self):
        while True:
            try:
                # i2c에서 5Byte 데이터를 읽음 (0번 더미, 1번이 ADC0/VR)
                adc_data = self.bus.read_i2c_block_data(self.i2c_address, self.command, 5)
                val = adc_data[1]
                
                # 0~255 -> 0~100으로 변환
                new_volume = int(val * 100 / 255)
                
                # 1 이상의 변화가 있을 때만 GUI 및 오디오 시스템 갱신
                if abs(new_volume - self.volume) >= 1:
                    self.volume = new_volume
                    if self.callback:
                        self.callback(self.volume)
            except Exception as e:
                # 센서 통신 에러 무시 (I2C 간헐적 실패 대응)
                pass
            
            # 폴링 주기
            time.sleep(0.1)
