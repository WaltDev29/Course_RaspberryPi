from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
import sys

# 스위치 GPIO 핀 번호
SW1_PIN = 4
SW2_PIN = 17
SW3_PIN = 18
SW4_PIN = 22

SW_PIN_LIST = [SW1_PIN, SW2_PIN, SW3_PIN, SW4_PIN]


class MainFrame(Frame):

    def __init__(self, master):

        master.title('Switch Keypad Control Example')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x280+10+10")

        # 키패드의 textvariable 옵션에 사용될 상태 저장 변수 리스트
        self.buttonState = [
            StringVar(),
            StringVar(),
            StringVar(),
            StringVar()
        ]

        for i in range(len(self.buttonState)):
            self.buttonState[i].set(
                "SW " + str(i + 1) + "\n[X]"
            )

        # 키패드 상태를 표시할 라벨 위젯 리스트
        self.keyapdLabel = []

        for i in range(len(SW_PIN_LIST)):

            self.keyapdLabel.append(
                Label(
                    master,
                    background="yellow",
                    textvariable=self.buttonState[i]
                )
            )

            self.keyapdLabel[i].pack(
                side=LEFT,
                expand=1
            )

        # 실시간으로 상태를 변경시키는 스레드 생성
        keypadthread = threading.Thread(
            target=self.KeypadStateThread
        )

        keypadthread.start()

    # 키패드의 상태를 확인한다.
    def KeypadStateThread(self):

        try:

            # 스레드는 반복하며 상태를 체크한다.
            while True:

                for i in range(len(self.buttonState)):

                    # 키패드는 눌렸을 때 0이 된다.
                    if GPIO.input(SW_PIN_LIST[i]) == 0:

                        # textvariable 값을 변경하면
                        # 라벨 값도 자동으로 변경된다.
                        self.buttonState[i].set(
                            "SW " + str(i + 1) + "\n[O]"
                        )

                    else:

                        self.buttonState[i].set(
                            "SW " + str(i + 1) + "\n[X]"
                        )

                time.sleep(0.1)

        except Exception as err:

            time.sleep(1)
            print(err)


# GPIO를 사용하기 전 초기화하는 함수
def GPIO_Keypad_init():

    # BCM 핀맵 사용
    GPIO.setmode(GPIO.BCM)

    for p_index in SW_PIN_LIST:

        GPIO.setup(
            p_index,
            GPIO.IN
        )


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':

    GPIO_Keypad_init()

    root = Tk()                    # 창 객체 생성
    mainFrame = MainFrame(root)    # MainFrame 객체 생성

    root.mainloop()                # 이벤트 처리

    GPIO.cleanup()                 # GPIO 초기화

    sys.exit()                     # 프로그램 종료