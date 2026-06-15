from tkinter import *
import Adafruit_DHT
import time
import threading
import sys

# DHT11 센서 설정
sensor = Adafruit_DHT.DHT11
pin = 27


# 프로그램의 창을 생성하는 MainFrame 클래스
class MainFrame(Frame):

    # MainFrame 클래스의 생성자
    # self는 객체의 인스턴스를 의미하며,
    # master는 부모 객체를 의미한다.
    # 여기서는 Tk를 의미한다.
    def __init__(self, master):

        master.title('Temperature, Humidity Example')

        # 윈도우 크기 및 좌표 설정
        master.geometry("400x240+10+10")

        # 온습도 센서의 값을 저장하는 변수
        self.value = StringVar()

        # Label은 textvariable 옵션을 통해
        # 넘긴 변수(value)로 데이터를 변경한다.
        self.value.set(
            'Temp={}°C Humidity={}%'.format('-', '-')
        )

        # 온습도 센서의 상태를 표시할 Label 위젯
        self.tempLabel = Label(
            master,
            background="yellow",
            textvariable=self.value
        )

        self.tempLabel.pack(
            side=LEFT,
            expand=1
        )

        # 실시간으로 상태를 변경시키는 스레드 생성
        self.t = threading.Thread(
            target=self.analogReadThread
        )

        self.t.start()

    # 온습도 센서를 이용해 온습도 값을 측정하는 스레드
    def analogReadThread(self):

        try:

            # 스레드는 반복하며 온습도를 측정한다.
            while True:

                # 온습도 데이터를 센서로부터 가져온다.
                humidity, temperature = Adafruit_DHT.read(
                    sensor,
                    pin
                )

                if humidity is not None and temperature is not None:

                    # Label의 온습도 값을 변경한다.
                    self.value.set(
                        'Temp={}°C Humidity={}%'.format(
                            temperature,
                            humidity
                        )
                    )

                else:

                    print(
                        humidity,
                        temperature
                    )

                # 1초 대기
                time.sleep(1)

        except Exception as err:

            time.sleep(1)

            print(err)


# 프로그램의 메인에 해당하는 최상위 구문
if __name__ == '__main__':

    root = Tk()                  # 창을 띄우기 위한 객체 선언

    mainFrame = MainFrame(root)  # MainFrame 객체 생성

    root.mainloop()              # 이벤트 처리 수행

    sys.exit()                   # 프로그램 완전 종료