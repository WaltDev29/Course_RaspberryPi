from tkinter import *
import smbus
import sys

RED_LED = 0b00000001
GREEN_LED = 0b00000010
BLUE_LED = 0b00000100


class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=1)

        master.title('LED Control Example')
        master.geometry("400x240+10+10")

        # RED
        Button(self, background="red", text="RED LED ON",
               command=lambda: self.onButtonClickEvent(0)).pack(expand=1)
        Button(self, background="red", text="RED LED OFF",
               command=lambda: self.onButtonClickEvent(1)).pack(expand=1)

        # GREEN
        Button(self, background="green", text="GREEN LED ON",
               command=lambda: self.onButtonClickEvent(2)).pack(expand=1)
        Button(self, background="green", text="GREEN LED OFF",
               command=lambda: self.onButtonClickEvent(3)).pack(expand=1)

        # BLUE
        Button(self, background="blue", text="BLUE LED ON",
               command=lambda: self.onButtonClickEvent(4)).pack(expand=1)
        Button(self, background="blue", text="BLUE LED OFF",
               command=lambda: self.onButtonClickEvent(5)).pack(expand=1)

        self.ledInit()

    def onButtonClickEvent(self, pin):
        if pin == 0:
            self.ledOn(RED_LED)
        elif pin == 1:
            self.ledOff(RED_LED)
        elif pin == 2:
            self.ledOn(GREEN_LED)
        elif pin == 3:
            self.ledOff(GREEN_LED)
        elif pin == 4:
            self.ledOn(BLUE_LED)
        elif pin == 5:
            self.ledOff(BLUE_LED)

    def ledInit(self):
        self.state = 0b00000000
        self.bus = smbus.SMBus(1)

    def ledOn(self, cmd):
        self.state = self.state | cmd
        self.bus.write_byte(0x20, self.state)

    def ledOff(self, cmd):
        self.state = self.state & (~cmd)
        self.bus.write_byte(0x20, self.state)


if __name__ == '__main__':
    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()
    sys.exit()