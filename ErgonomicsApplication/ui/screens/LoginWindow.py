# ui/screens/LoginWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame
from app.services import Services

services = Services()

class LoginWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Вход", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        tk.Label(self, text="Имя пользователя:", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=10, padx=20)

        tk.Label(self, text="Пароль:", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=10, padx=20)

        login_button = tk.Button(
            self,
            text="Войти",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=self.login
        )
        login_button.pack(pady=20)

        back_button = tk.Button(
            self,
            text="Назад",
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#0047ab",
            activebackground="#f1f1f1",
            activeforeground="#0047ab",
            command=lambda: master.window_manager.show_frame("AuthWindow")
        )
        back_button.place(x=10, y=10)

        self.error_label = tk.Label(self, text="", fg="red", bg="#f7f7f7", font=("Arial", 12))
        self.error_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        result = services.user.check_user(login=username, password=password)

        if result is None:
            self.error_label.config(text="Неверный логин или пароль!")
            return

        FIO, user_id = result

        self.master.window_manager.current_user_id = user_id
        print(f"[DEBUG] Авторизация прошла успешно. user_id={user_id}")

        self.master.window_manager.show_frame("MainWindow", FIO=FIO)
