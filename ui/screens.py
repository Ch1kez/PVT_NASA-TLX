import random
import time
import tkinter as tk

from pydantic import ValidationError

from app.schemas import UserSchema
from app.services import Services as services


class CenteredFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        # Центрируем основной контейнер
        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def add_to_container(self, widget):
        """Добавляет виджет в контейнер для удобства."""
        widget.pack(pady=10)


# Auth Window
class AuthWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Добро пожаловать!", font=("Arial", 16)).pack(pady=20)

        login_button = tk.Button(self, text="Вход", command=lambda: master.window_manager.show_frame("LoginWindow"))
        login_button.pack(pady=5)

        register_button = tk.Button(self, text="Зарегистрироваться",
                                    command=lambda: master.window_manager.show_frame("RegisterWindow"))
        register_button.pack(pady=5)


# Register Window
class RegisterWindow(CenteredFrame):

    def __init__(self, master):
        super().__init__(master)
        self.services = services

        # Поля ввода
        tk.Label(self, text="ФИО").pack()
        self.FIO_entry = tk.Entry(self)
        self.FIO_entry.pack()

        tk.Label(self, text="Логин").pack()
        self.login_entry = tk.Entry(self)
        self.login_entry.pack()
        self.login_entry.bind("<KeyRelease>", self.validate_login)

        tk.Label(self, text="Пароль").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()
        self.password_entry.bind("<KeyRelease>", self.validate_passwords)


        tk.Label(self, text="Подтвердите пароль").pack()
        self.confirm_password_entry = tk.Entry(self, show="*")
        self.confirm_password_entry.pack()
        self.confirm_password_entry.bind("<KeyRelease>", self.validate_passwords)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

        self.register_button = tk.Button(self, text="Регистрация", command=self.register)
        self.register_button.pack()

    def validate_login(self, event=None):
        """Валидация логина на лету."""
        login = self.login_entry.get()
        if len(login) < 3 or len(login) > 50:
            self.error_label.config(text="Логин должен быть от 3 до 50 символов")
        else:
            self.error_label.config(text="")

    def validate_passwords(self, event=None):
        """Валидация совпадения пароля."""
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if len(password) < 4:
            self.error_label.config(text="Пароль слишком короткий!")
        elif password != confirm_password:
            self.error_label.config(text="Пароли не совпадают!")
        else:
            self.error_label.config(text="")

    def register(self):
        """Обработчик регистрации."""
        FIO = self.FIO_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        # Очистка ошибок
        self.error_label.config(text="")

        # Проверка совпадения паролей
        if password != confirm_password:
            self.error_label.config(text="Пароли не совпадают!")
            return

        # Данные для регистрации
        user_data = {
            "name": FIO,
            "login": login,
            "password": password,
        }

        # Валидация через Pydantic
        try:
            validated_data = UserSchema(**user_data)
            self.services.user.create_user(user_data=validated_data.dict())
            tk.Label(self, text="Успешно зарегистрирован!", fg="green").pack()
            self.master.window_manager.show_frame("MainWindow")
        except ValidationError as e:
            # Отображение первой ошибки валидации
            first_error = e.errors()[0]
            field = first_error["loc"][0]
            message = first_error["msg"]
            self.error_label.config(text=f"Ошибка в поле '{field}': {message}")
        except Exception as e:
            # Отображение других ошибок
            self.error_label.config(text=f"Возникла ошибка: {e}")


# Login Window
class LoginWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Вход").pack(pady=10)

        tk.Label(self, text="Имя пользователя:").pack()
        self.username_entry = tk.Entry(self)
        self.username_entry.pack()

        tk.Label(self, text="Пароль:").pack()
        self.password_entry = tk.Entry(self, show="*")
        self.password_entry.pack()

        tk.Button(self, text="Войти", command=self.login).pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        user_id = True  # Для теста, заменить на реальную логику авторизации

        if user_id:
            self.master.window_manager.show_frame("MainWindow")
        else:
            tk.Label(self, text="Неверные данные!").pack()


# Main Window
class MainWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Эргономическая оценка кабины самолета", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Пройти PVT тест", command=lambda: master.window_manager.show_frame("PVTWindow")).pack(
            pady=10)
        tk.Button(self, text="Пройти NASA-TLX тест",
                  command=lambda: master.window_manager.show_frame("NASA_TLXWindow")).pack(pady=10)
        tk.Button(self, text="Результаты тестов",
                  command=lambda: master.window_manager.show_frame("ResultsWindow")).pack(pady=10)
        tk.Button(self, text="Отчёты", command=lambda: master.window_manager.show_frame("ReportWindow")).pack(pady=10)


# PVT Test Window
class PVTWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Нажмите 'СТАРТ', чтобы начать тест.", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_button = tk.Button(self, text="СТАРТ", command=self.start_test)
        self.start_button.pack(pady=10)

        self.react_button = tk.Button(self, text="РЕАГИРУЙТЕ", state=tk.DISABLED, command=self.record_reaction_time)
        self.react_button.pack(pady=10)

        self.start_time = None

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)
        self.react_button.config(state=tk.DISABLED)
        self.label.config(text="Подождите...")
        self.update()

        delay = random.uniform(2, 5)
        self.after(int(delay * 1000), self.enable_reaction_phase)

    def enable_reaction_phase(self):
        self.label.config(text="НАЖМИТЕ 'РЕАГИРУЙТЕ'!")
        self.react_button.config(state=tk.NORMAL)
        self.start_time = time.time()

    def record_reaction_time(self):
        if self.start_time:
            reaction_time = time.time() - self.start_time
            self.label.config(text=f"Ваше время реакции: {reaction_time:.3f} сек.")
            self.start_button.config(state=tk.NORMAL)
            self.react_button.config(state=tk.DISABLED)


# NASA-TLX Window
class NASA_TLXWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.labels = ["Mental Demand", "Physical Demand", "Temporal Demand", "Performance", "Effort", "Frustration"]
        self.entries = {}

        for label in self.labels:
            tk.Label(self, text=label, font=("Arial", 12)).pack(pady=5)
            entry = tk.Entry(self)
            entry.pack(pady=5)
            self.entries[label] = entry

        tk.Button(self, text="Сохранить результаты", command=self.save_results).pack(pady=20)

    def save_results(self):
        results = {label: entry.get() for label, entry in self.entries.items()}
        print("Результаты NASA-TLX:", results)


# Report Window
class ReportWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Ваши результаты:", font=("Arial", 14)).pack(pady=10)

        self.listbox = tk.Listbox(self, width=50, height=10)
        self.listbox.pack(pady=10)
        self.load_results()

    def load_results(self):
        results = [
            {'Mental Demand': 123, 'Physical Demand': 123, 'Temporal Demand': 123, 'Performance': 123, 'Effort': 123,
             'Frustration': 123}]
        for result in results:
            self.listbox.insert(tk.END, "".join(f'{key}: {val}, ' for key, val in result.items()))


class ResultsWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Результаты тестов", font=("Arial", 16)).pack(pady=20)
        text = tk.Text(self)
        text.pack(fill=tk.BOTH, expand=True)


if __name__ == "__main__":
    from ui.window_manager import WindowManager

    root = tk.Tk()
    root.geometry("800x600")
    window_manager = WindowManager(root)
    root.window_manager = window_manager

    # Register all frames
    window_manager.create_and_register("AuthWindow", AuthWindow)
    window_manager.create_and_register("LoginWindow", LoginWindow)
    window_manager.create_and_register("RegisterWindow", RegisterWindow)
    window_manager.create_and_register("MainWindow", MainWindow)
    window_manager.create_and_register("PVTWindow", PVTWindow)
    window_manager.create_and_register("NASA_TLXWindow", NASA_TLXWindow)
    window_manager.create_and_register("ReportWindow", ReportWindow)
    window_manager.create_and_register("ResultsWindow", ResultsWindow)

    window_manager.show_frame("AuthWindow")
    root.mainloop()
