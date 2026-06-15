from tkinter import *

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)

        master.title('창')
        master.geometry("320x240+10+10")

        entry = Entry(master, background="magenta")
        entry.pack(expand=1)


if __name__ == '__main__':
    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()