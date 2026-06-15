from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
import sys

# 스텝모터와 연결된 GPIO 번호를 변수에 저장한다.
STEP_IN1 = 16
STEP_IN2 = 20
STEP_IN3 = 21
STEP_IN4 = 26

pinsArray = [STEP_IN1, STEP_IN2, STEP_IN3, STEP_IN4]

# 풀 스텝 구동 (1상 여자 방식)
signal_full = [
    [GPIO.HIGH, GPIO.LOW, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.HIGH, GPIO.LOW, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.HIGH, GPIO.LOW],
    [GPIO.LOW, GPIO.LOW, GPIO.LOW, GPIO.HIGH]
]

# 1스텝의 사이클
FULL_STEP = len(pinsArray)

ROTATE_360_STEP = 512   # FULL_STEP으로 512스텝
MOTOR_SPEED = 100       # 0 ~ 100

# 스태핑모터 상태에 대한 변수 (global 변수)
state = 'STOP'


# 프로그램의 창을 생성하는 MainFrame 클래스
class MainFrame(Frame):

    # MainFrame 클래스의 생성자
    # self는 객체의 인스턴스를 의미하며,
    # master는 부모 객체를 의미한다. 여기서는 Tk를 의미한다.
    def __init__(self, master):
        master.title('Stepping Motor Control Example')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x240+10+10")

        self.t = threading.Thread(
            target=self.stepControlFunctionThread
        )
        self.t.start()

        # 버튼 객체 리스트
        button = []

        button.append(
            Button(
                master,
                background="cyan",
                text="Clockwise ↻",
                command=lambda: self.onButtonClickEvent(0)
            )
        )
        button[0].pack(side=LEFT, expand=1)

        button.append(
            Button(
                master,
                background="cyan",
                text="STOP",
                command=lambda: self.onButtonClickEvent(1)
            )
        )
        button[1].pack(side=LEFT, expand=1)

        button.append(
            Button(
                master,
                background="cyan",
                text="Count Clockwise ↺",
                command=lambda: self.onButtonClickEvent(2)
            )
        )
        button[2].pack(side=LEFT, expand=1)

    def onButtonClickEvent(self, pin):
        global state

        if pin == 0:
            state = 'CW'

        elif pin == 1:
            state = 'STOP'

        elif pin == 2:
            state = 'CCW'

    def Run_Steps(self, isCwDirection, stepvalue, speed):
        global state

        if speed >= 100:
            speed = 100

        if speed != 0:
            speedValue = 0.2 / speed
        else:
            speedValue = 0

        if isCwDirection:
            state = "CW"
        else:
            state = "CCW"

        for i in range(0, stepvalue):

            # 정방향
            if isCwDirection:

                for step_idx in range(FULL_STEP):

                    if state != 'CW':
                        break

                    self.sendSignal(step_idx)
                    time.sleep(speedValue)

            # 역방향
            else:

                for step_idx in reversed(range(FULL_STEP)):

                    if state != 'CCW':
                        break

                    self.sendSignal(step_idx)
                    time.sleep(speedValue)

    # 스텝에 따라 시그널을 발생시킨다.
    def sendSignal(self, step_idx):

        for idx in range(4):
            GPIO.output(
                pinsArray[idx],
                signal_full[step_idx][idx]
            )

    # 아래 함수가 스레드로 주기적으로 구동되며 상태에 따른 동작을 수행한다.
    def stepControlFunctionThread(self):
        global state

        try:
            while True:

                if state == 'CW':

                    self.Run_Steps(
                        True,
                        ROTATE_360_STEP,
                        MOTOR_SPEED
                    )

                    state = "STOP"

                elif state == 'STOP':

                    for p_index in pinsArray:
                        GPIO.output(p_index, GPIO.LOW)

                elif state == 'CCW':

                    self.Run_Steps(
                        False,
                        ROTATE_360_STEP,
                        MOTOR_SPEED
                    )

                    state = "STOP"

        except:
            time.sleep(0.1)


# GPIO를 사용하기 전 초기화하는 함수
def GPIO_STEP_init():

    # BCM 핀맵을 사용한다.
    GPIO.setmode(GPIO.BCM)

    for p_index in pinsArray:
        GPIO.setup(p_index, GPIO.OUT)
        GPIO.output(p_index, GPIO.LOW)


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':

    GPIO_STEP_init()

    root = Tk()                 # 창을 띄우기 위한 객체
    mainFrame = MainFrame(root) # MainFrame 객체 생성

    root.mainloop()             # 이벤트 처리

    GPIO.cleanup()              # GPIO 초기화
    sys.exit()                  # 프로그램 종료