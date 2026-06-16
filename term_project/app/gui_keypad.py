import tkinter as tk

class VirtualKeypadWindow:
    def __init__(self, parent, on_pad_press=None):
        self.on_pad_press = on_pad_press
        self.window = tk.Toplevel(parent)
        self.window.title("Virtual Keypad")
        self.window.geometry("250x300")
        self.window.configure(bg='#2b2b2b')
        self.window.resizable(False, False)
        
        # 3열 4행의 서로 다른 색상 목록
        colors = ['red', 'green', 'dodger blue', 'orange', 'purple', 'cyan', 'magenta', 'yellow', 'pink', 'brown', 'lime green', 'teal']
        
        def on_press(event, btn, color, key_num):
            # 클릭 시 배경색과 activebackground(누르고 있을 때의 색상)를 모두 대상 색상으로 변경
            btn.config(bg=color, activebackground=color)
            if self.on_pad_press:
                self.on_pad_press(key_num)
            
        def on_release(event, btn):
            # 뗐을 때 다시 원래 색상으로 복구 (activebackground도 동일하게 맞춰 마우스 호버 효과 제거)
            btn.config(bg='#4a4a4a', activebackground='#4a4a4a')
            
        self.buttons = {}
        for row in range(4):
            self.window.rowconfigure(row, weight=1)
            for col in range(3):
                self.window.columnconfigure(col, weight=1)
                idx = row * 3 + col
                btn_color = colors[idx]
                key_num = idx + 1
                
                # 버튼 생성 시 activebackground를 bg와 똑같이 맞춰 마우스를 올렸을 때(Hover) 색상이 변하지 않도록 설정
                btn = tk.Button(self.window, bg='#4a4a4a', activebackground='#4a4a4a', fg='white', font=('Arial', 14, 'bold'))
                btn.grid(row=row, column=col, sticky='nsew', padx=5, pady=5)
                
                # 좌클릭 누름/뗌 이벤트 바인딩
                btn.bind('<ButtonPress-1>', lambda e, b=btn, c=btn_color, k=key_num: on_press(e, b, c, k))
                btn.bind('<ButtonRelease-1>', lambda e, b=btn: on_release(e, b))
                
                # 외부 하드웨어 이벤트 제어를 위해 딕셔너리에 저장
                self.buttons[key_num] = (btn, btn_color)
                
    def highlight_button(self, key_num):
        """하드웨어 키패드가 눌렸을 때 외부에서 호출하여 색상 변경"""
        if key_num in self.buttons:
            btn, color = self.buttons[key_num]
            btn.config(bg=color, activebackground=color)
            
    def unhighlight_button(self, key_num):
        """하드웨어 키패드에서 손을 뗐을 때 외부에서 호출하여 색상 복구"""
        if key_num in self.buttons:
            btn, _ = self.buttons[key_num]
            btn.config(bg='#4a4a4a', activebackground='#4a4a4a')
