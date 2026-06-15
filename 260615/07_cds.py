from tkinter import *
import RPi.GPIO as GPIO
import smbus
import time
import threading
import sys

# I2C 설정
bus = smbus.SMBus(1)
i2c_address = 0x48
command = 0x44


class MainFrame(Frame):

    # MainFrame 클래스의 생성자
    # self는 객체의 인스턴스를 의미하며,
    # master는 부모 객체를 의미한다. 여기서는 Tk를 의미한다.
    def __init__(self, master):

        master.title('LightSensor(CdS) Monitoring')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x240+10+10")

        # 조도센서 값을 저장하는 변수
        self.value = StringVar()

        # Label은 textvariable 옵션을 통해
        # 넘긴 변수(value)로 데이터를 변경한다.
        self.value.set(
            "조도센서 : {}%".format(0)
        )

        # 조도센서의 상태를 표시할 Label
        self.cds_label = Label(
            master,
            background="yellow",
            textvariable=self.value
        )

        self.cds_label.pack(
            side=LEFT,
            expand=1
        )

        # 실시간으로 상태를 변경시키는 스레드 생성
        self.t = threading.Thread(
            target=self.analogReadThread
        )

        self.t.start()

    def analogReadThread(self):

        try:

            while True:

                # i2c 주소와 명령어를 전송하여
                # 5Byte의 데이터를 읽어온다.
                # [dummy, A0, A1, A2, A3]

                adc_data = bus.read_i2c_block_data(
                    i2c_address,
                    command,
                    5
                )

                # I2C로부터 센서 값을 읽어온다.
                # CdS 센서는 2번 채널(A1)
                cds_value = adc_data[2]

                # 0~255 -> 0~100%
                cds_value = cds_value * 100 / 255

                # 소수 둘째 자리까지 표시
                cds_value = round(cds_value, 2)

                # Label 값 변경
                self.value.set(
                    "조도센서 : {}%".format(cds_value)
                )

                time.sleep(0.1)

        except Exception as err:

            time.sleep(1)

            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':

    root = Tk()                  # 창 객체 생성

    mainFrame = MainFrame(root)  # MainFrame 객체 생성

    root.mainloop()              # 이벤트 처리

    sys.exit()                   # 프로그램 종료