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

# Servo 설정
SERVO_PIN = 25

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

servo_pwm = GPIO.PWM(SERVO_PIN, 50)
servo_pwm.start(0)


class MainFrame(Frame):

    def __init__(self, master):

        master.title('VR -> Servo Control')

        master.geometry("400x240+10+10")

        self.value = StringVar()

        self.value.set(
            "VR : 0%\nAngle : 0°"
        )

        self.VrLabel = Label(
            master,
            background="yellow",
            textvariable=self.value,
            font=("Arial", 15)
        )

        self.VrLabel.pack(
            side=LEFT,
            expand=1
        )

        self.t = threading.Thread(
            target=self.analogReadThread,
            daemon=True
        )

        self.t.start()

    def analogReadThread(self):

        try:

            while True:

                adc_data = bus.read_i2c_block_data(
                    i2c_address,
                    command,
                    5
                )

                # VR 값 읽기 (A0)
                VrValue = adc_data[1]

                # 0~255 -> 0~100%
                VrValue = VrValue * 100 / 255

                VrValue = round(VrValue, 1)

                # 0~100 -> -90~90
                angle = VrValue * 180 / 100 - 90

                angle = round(angle, 1)

                # 각도 -> Duty Cycle
                duty = (angle + 90) / 18 + 2.5

                servo_pwm.ChangeDutyCycle(duty)

                # 화면 출력
                self.value.set(
                    "VR : {}%\nAngle : {}°".format(
                        VrValue,
                        angle
                    )
                )

                time.sleep(0.1)

        except Exception as err:

            print(err)


if __name__ == '__main__':

    try:

        root = Tk()

        mainFrame = MainFrame(root)

        root.mainloop()

    finally:

        servo_pwm.stop()

        GPIO.cleanup()

        sys.exit()