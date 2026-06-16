import tkinter as tk

class VirtualKeypadWindow:
    def __init__(self, parent):
        self.window = tk.Toplevel(parent)
        self.window.title("Virtual Keypad")
        self.window.geometry("250x300")
        self.window.configure(bg='#2b2b2b')
        self.window.resizable(False, False)
        
        # 3열 4행의 서로 다른 색상 목록
        colors = ['red', 'green', 'dodger blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'pink', 'brown', 'lime green', 'teal']
        
        def on_press(event, btn, color):
            btn.config(bg=color)
            
        def on_release(event, btn):
            btn.config(bg='#4a4a4a')
            
        for row in range(4):
            self.window.rowconfigure(row, weight=1)
            for col in range(3):
                self.window.columnconfigure(col, weight=1)
                idx = row * 3 + col
                btn_color = colors[idx]
                
                # 버튼(ttk 말고 tk 사용해야 색상변경이 쉬움)
                btn = tk.Button(self.window, text=str(idx+1), bg='#4a4a4a', fg='white', font=('Arial', 14, 'bold'))
                btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
                
                # 좌클릭 누름/뗌 이벤트 바인딩
                btn.bind('<ButtonPress-1>', lambda e, b=btn, c=btn_color: on_press(e, b, c))
                btn.bind('<ButtonRelease-1>', lambda e, b=btn: on_release(e, b))
