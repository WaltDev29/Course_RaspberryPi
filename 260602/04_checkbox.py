from tkinter import *

class MainFrame(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(expand=1)

        master.title('창')
        master.geometry("320x240+10+10")

        self.checkbuttonvar = IntVar()

        checkbutton = Checkbutton(
            self,
            background="orange",
            text="CheckButton",
            variable=self.checkbuttonvar
        )
        checkbutton.pack(side=LEFT, expand=1)


if __name__ == '__main__':
    root = Tk()
    mainFrame = MainFrame(root)
    root.mainloop()