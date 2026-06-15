from tkinter import *
import RPi.GPIO as GPIO
import time
import threading
import sys

MOTOR_P = 19
MOTOR_M = 13


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=1)

        master.title('DC Motor Control Example')
        master.geometry("400x240+10+10")

        self.state = "STOP"

        # 스레드 시작
        dcmotorthread = threading.Thread(target=self.dc_motor_thread, daemon=True)
        dcmotorthread.start()

        # 버튼들
        Button(self, background="cyan", text="Clockwise",
               command=lambda: self.onButtonClickEvent(0)).pack(side=LEFT, expand=1)

        Button(self, background="cyan", text="STOP",
               command=lambda: self.onButtonClickEvent(1)).pack(side=LEFT, expand=1)

        Button(self, background="cyan", text="Counter Clockwise",
               command=lambda: self.onButtonClickEvent(2)).pack(side=LEFT, expand=1)

    def onButtonClickEvent(self, pin):
        if pin == 0:
            self.state = 'CW'
        elif pin == 1:
            self.state = 'STOP'
        elif pin == 2:
            self.state = 'CCW'

    def dc_motor_thread(self):
        try:
            while True:
                if self.state == 'CW':
                    GPIO.output(MOTOR_P, GPIO.HIGH)
                    GPIO.output(MOTOR_M, GPIO.LOW)

                elif self.state == 'STOP':
                    GPIO.output(MOTOR_P, GPIO.LOW)
                    GPIO.output(MOTOR_M, GPIO.LOW)

                elif self.state == 'CCW':
                    GPIO.output(MOTOR_P, GPIO.LOW)
                    GPIO.output(MOTOR_M, GPIO.HIGH)

                time.sleep(0.1)
        except:
            time.sleep(1)


def gpio_dcMotor_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(MOTOR_P, GPIO.OUT)
    GPIO.setup(MOTOR_M, GPIO.OUT)
    GPIO.output(MOTOR_P, GPIO.LOW)
    GPIO.output(MOTOR_M, GPIO.LOW)


def gpio_dcMotor_cleanup():
    GPIO.output(MOTOR_P, GPIO.LOW)
    GPIO.output(MOTOR_M, GPIO.LOW)
    GPIO.cleanup()


if __name__ == '__main__':
    gpio_dcMotor_init()

    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()

    gpio_dcMotor_cleanup()
    sys.exit()