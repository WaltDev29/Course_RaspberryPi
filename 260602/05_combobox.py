from tkinter import *
from tkinter import ttk

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=1)

        master.title('창')
        master.geometry("320x240+10+10")

        values = ['라면', '짜장면', '국수', '냉면', '짬뽕']

        combobox = ttk.Combobox(self, height=15, values=values)
        combobox.set("선택")
        combobox.pack(expand=1)


if __name__ == '__main__':
    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()