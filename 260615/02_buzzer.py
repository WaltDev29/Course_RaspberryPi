from tkinter import *
import RPi.GPIO as GPIO
import time
import sys

# Buzzer 핀에 대한 정의
buzzer = 12

# 4옥타브 도레미 ~ 5옥타브 도
SCALE = [261, 294, 330, 349, 392, 440, 493, 523]


# 프로그램의 창을 생성하는 MainFrame 클래스
class MainFrame(Frame):

    # MainFrame 클래스의 생성자
    # self는 객체의 인스턴스를 의미하며,
    # master는 부모 객체를 의미한다. 여기서는 Tk를 의미한다.
    def __init__(self, master):

        master.title('Buzzer Control Example')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x240+10+10")

        # 체크 버튼의 상태 값을 저장하는 변수
        self.checkbuttonvar = IntVar()

        # 체크 버튼 객체
        checkbutton = Checkbutton(
            master,
            background="orange",
            text="Buzzer",
            variable=self.checkbuttonvar,
            command=lambda: self.onCheckbuttonClickEvent()
        )

        checkbutton.pack(side=LEFT, expand=1)

        self.gpio_buzzer_init()

    def onCheckbuttonClickEvent(self):

        print("--------------------")

        # 입력 받은 값에 대한 이벤트 처리
        # 1일 시 HIGH, 0일 시 LOW
        if self.checkbuttonvar.get() == 1:

            self.pwm.ChangeDutyCycle(50)
            self.pwm.ChangeFrequency(SCALE[5])  # 주파수 변경

            print(str(buzzer) + " PIN HIGH")

        else:

            # 부저 끄기
            self.pwm.ChangeDutyCycle(100)

            print(str(buzzer) + " PIN LOW")

        print("--------------------")

    def gpio_buzzer_init(self):

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(buzzer, GPIO.OUT)
        GPIO.output(buzzer, GPIO.LOW)

        self.pwm = GPIO.PWM(buzzer, SCALE[0])

        # PWM 시작
        self.pwm.start(100)

    def gpio_buzzer_cleanup(self):

        GPIO.output(buzzer, GPIO.LOW)

        # PWM 종료
        self.pwm.stop()

        GPIO.cleanup()


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':

    root = Tk()                      # 창을 띄우기 위한 객체 선언
    mainFrame = MainFrame(root)      # MainFrame 객체 생성

    root.mainloop()                  # 이벤트 처리

    mainFrame.gpio_buzzer_cleanup()  # GPIO 정리

    sys.exit()                       # 프로그램 완전 종료