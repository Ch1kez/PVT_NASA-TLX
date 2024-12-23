# ui/screens/RegisterWindow.py
import tkinter as tk
from pydantic import ValidationError
from ui.components.CenteredFrame import CenteredFrame
from app.services import Services

services = Services()


class RegisterWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.services = services
        self.configure(bg="#f7f7f7")

        tk.Label(self, text="Регистрация", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)

        tk.Label(self, text="ФИО", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack()
        self.FIO_entry = tk.Entry(self, font=("Arial", 14))
        self.FIO_entry.pack(pady=5)

        tk.Label(self, text="Имя пользователя:", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack()
        self.login_entry = tk.Entry(self, font=("Arial", 14))
        self.login_entry.pack(pady=5)
        self.login_entry.bind("<KeyRelease>", self.validate_login)

        tk.Label(self, text="Пароль", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack()
        self.password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.password_entry.pack(pady=5)
        self.password_entry.bind("<KeyRelease>", self.validate_passwords)

        tk.Label(self, text="Подтвердите пароль", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack()
        self.confirm_password_entry = tk.Entry(self, show="*", font=("Arial", 14))
        self.confirm_password_entry.pack(pady=5)
        self.confirm_password_entry.bind("<KeyRelease>", self.validate_passwords)

        self.error_label = tk.Label(self, text="", fg="red", bg="#f7f7f7", font=("Arial", 12))
        self.error_label.pack(pady=10)

        self.register_button = tk.Button(
            self,
            text="Регистрация",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=self.register
        )
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(
            self,
            text="Назад",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: master.window_manager.show_frame("AuthWindow")
        )
        self.back_button.place(x=10, y=10)

    def validate_login(self, event=None):
        login = self.login_entry.get()
        if len(login) < 3 or len(login) > 50:
            self.error_label.config(text="Логин должен быть от 3 до 50 символов")
        else:
            try:
                if self.services.user.is_login_exists(login):
                    self.error_label.config(text="Логин уже используется!")
            except Exception as e:
                self.error_label.config(text=f"Ошибка проверки логина: {e}")

    def validate_passwords(self, event=None):
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if len(password) < 4:
            self.error_label.config(text="Пароль слишком короткий!")
        elif password != confirm_password:
            self.error_label.config(text="Пароли не совпадают!")
        else:
            self.error_label.config(text="")

    def register(self):
        FIO = self.FIO_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        self.error_label.config(text="")

        if password != confirm_password:
            self.error_label.config(text="Пароли не совпадают!")
            return

        user_data = {"name": FIO, "login": login, "password": password}

        try:
            user_id = self.services.user.create_user(user_data=user_data)
            self.master.window_manager.current_user_id = user_id
            print(f"[DEBUG] Регистрация прошла успешно. user_id={user_id}")

            tk.Label(self, text="Успешно зарегистрирован!", fg="green", bg="#f7f7f7", font=("Arial", 14)).pack()
            self.master.window_manager.show_frame("MainWindow", FIO=FIO)
        except ValidationError as e:
            first_error = e.errors()[0]
            field = first_error["loc"][0]
            message = first_error["msg"]
            self.error_label.config(text=f"Ошибка в поле '{field}': {message}")
        except ValueError as e:
            self.error_label.config(text=str(e))
        except Exception as e:
            self.error_label.config(text=f"Возникла ошибка: {e}")
