from tkinter import *
import RPi_I2C_driver
import sys

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=1)

        master.title('TextLCD Control Example')
        master.geometry("400x240+10+10")

        self.mylcd = RPi_I2C_driver.lcd()

        self.entryMessage_Line1 = StringVar()
        self.entryMessage_Line2 = StringVar()

        # Line 1 입력
        entry_Line1 = Entry(self, background="magenta",
                            textvariable=self.entryMessage_Line1)
        entry_Line1.pack(expand=1)

        sendButton1 = Button(self, background="cyan", text="Line-1 작성",
                             command=lambda: self.onButtonClickEvent(0))
        sendButton1.pack(expand=1)

        # Line 2 입력
        entry_Line2 = Entry(self, background="magenta",
                            textvariable=self.entryMessage_Line2)
        entry_Line2.pack(expand=1)

        sendButton2 = Button(self, background="cyan", text="Line-2 작성",
                             command=lambda: self.onButtonClickEvent(1))
        sendButton2.pack(expand=1)

    def onButtonClickEvent(self, pin):
        if pin == 0:
            text = self.entryMessage_Line1.get()
            self.mylcd.lcd_display_string(text, 1)
        elif pin == 1:
            text = self.entryMessage_Line2.get()
            self.mylcd.lcd_display_string(text, 2)


if __name__ == '__main__':
    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()
    sys.exit()