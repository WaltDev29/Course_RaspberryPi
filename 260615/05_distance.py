from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
import sys
import smbus

# 초음파 센서 핀 설정
trig = 23
echo = 24

# RGB LED 비트값
RED_LED = 0b00000001
GREEN_LED = 0b00000010
BLUE_LED = 0b00000100

# I2C Bus
bus = smbus.SMBus(1)

# RGB LED 주소
LED_ADDR = 0x20


# 프로그램의 창을 생성하는 MainFrame 클래스
class MainFrame(Frame):

    # MainFrame 클래스의 생성자
    # self는 객체의 인스턴스를 의미하며,
    # master는 부모 객체를 의미한다. 여기서는 Tk를 의미한다.
    def __init__(self, master):

        master.title('Ultrasonic Control Example')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x240+10+10")

        # 초음파 센서의 상태를 저장하는 변수
        self.buttonState = StringVar()

        # 초기 메시지
        self.buttonState.set("Distance : 0 cm")

        # 초음파 센서 상태를 표시할 Label
        self.usnLabel = Label(
            master,
            background="yellow",
            textvariable=self.buttonState
        )

        self.usnLabel.pack(
            side=BOTTOM,
            expand=1
        )

        # 거리 상태 색상 표시
        self.colorLabel = Label(
            master,
            width=10,
            height=5,
            background="blue"
        )

        self.colorLabel.pack(
            side=TOP,
            expand=1
        )

        # 실시간 거리 측정 스레드 생성
        self.t = threading.Thread(
            target=self.UltasonicStateThread
        )

        self.t.start()

    # 초음파 센서를 이용해 거리를 측정하는 스레드
    def UltasonicStateThread(self):

        try:

            while True:

                # 거리 측정을 위해 초음파 발사
                GPIO.output(trig, GPIO.LOW)
                time.sleep(0.5)

                GPIO.output(trig, GPIO.HIGH)
                time.sleep(0.00001)   # 10us

                GPIO.output(trig, GPIO.LOW)

                # Echo 신호 시작 시간
                while GPIO.input(echo) == 0:
                    signal_Start = time.time()

                # Echo 신호 종료 시간
                while GPIO.input(echo) == 1:
                    signal_End = time.time()

                # 거리 계산
                responseDuration = signal_End - signal_Start

                # 음속 : 34000 cm/s
                # 왕복 거리이므로 2로 나눈다.
                distance = responseDuration * 34000 / 2

                # 소수 둘째 자리까지 출력
                distance = round(distance, 2)

                # 1000cm 초과 시 출력하지 않음
                if distance < 1000:

                    self.buttonState.set(
                        "Distance : " +
                        str(distance) +
                        " cm"
                    )
                
                # 거리별 색상 변경
                if distance < 20:

                    self.colorLabel.config(
                        background="red"
                    )

                    # RGB LED 빨강
                    bus.write_byte(
                        LED_ADDR,
                        RED_LED
                    )

                elif distance <= 50:

                    self.colorLabel.config(
                        background="green"
                    )

                    # RGB LED 초록
                    bus.write_byte(
                        LED_ADDR,
                        GREEN_LED
                    )

                else:

                    self.colorLabel.config(
                        background="blue"
                    )

                    # RGB LED 파랑
                    bus.write_byte(
                        LED_ADDR,
                        BLUE_LED
                    )

                time.sleep(0.1)

        except Exception as err:

            time.sleep(1)

            print(err)


# GPIO를 사용하기 전 초기화하는 함수
def GPIO_Ultasonic_init():

    # BCM 핀맵 사용
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(trig, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.output(trig, GPIO.LOW)


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':
    try:
        GPIO_Ultasonic_init()
        root = Tk()                   # 창 객체 생성
        mainFrame = MainFrame(root)   # MainFrame 객체 생성
        root.mainloop()               # 이벤트 처리

    finally:
        # RGB LED 모두 켜기
        state = RED_LED | GREEN_LED | BLUE_LED

        bus.write_byte(
            LED_ADDR,
            state
        )

        GPIO.cleanup()
        sys.exit()