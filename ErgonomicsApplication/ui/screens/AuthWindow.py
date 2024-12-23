# ui/screens/AuthWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class AuthWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Добро пожаловать!", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)

        login_button = tk.Button(
            self,
            text="Вход",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: master.window_manager.show_frame("LoginWindow")
        )
        login_button.pack(pady=10)

        register_button = tk.Button(
            self,
            text="Зарегистрироваться",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: master.window_manager.show_frame("RegisterWindow")
        )
        register_button.pack(pady=10)

        tk.Label(self, text="© 2024, Ваша компания", bg="#f7f7f7", fg="#555").pack(side="bottom", pady=10)
