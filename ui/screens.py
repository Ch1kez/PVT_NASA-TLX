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


# Экраны авторизации
class AuthWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Добро пожаловать!", font=("Arial", 16)).pack(pady=20)

        login_button = tk.Button(self, text="Вход", command=lambda: master.window_manager.show_frame("LoginWindow"))
        login_button.pack(pady=5)

        register_button = tk.Button(self, text="Зарегистрироваться",
                                    command=lambda: master.window_manager.show_frame("RegisterWindow"))
        register_button.pack(pady=5)


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

        self.back_button = tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("AuthWindow"))
        self.back_button.place(x=10, y=10)

    def validate_login(self, event=None):
        login = self.login_entry.get()
        if len(login) < 3 or len(login) > 50:
            self.error_label.config(text="Логин должен быть от 3 до 50 символов")
        else:
            try:
                if services.user.is_login_exists(login):
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
            validated_data = UserSchema(**user_data)
            self.services.user.create_user(user_data=validated_data.dict())
            tk.Label(self, text="Успешно зарегистрирован!", fg="green").pack()
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
        self.back_button = tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("AuthWindow"))
        self.back_button.place(x=10, y=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        FIO = services.user.check_user(login=username, password=password)

        if FIO:
            self.master.window_manager.show_frame("MainWindow", FIO=FIO)
        else:
            tk.Label(self, text="Неверный логин или пароль!", fg="red").pack()


# Главное меню
class MainWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Эргономическая оценка кабины самолета", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Перейти к тестированию",
                  command=lambda: master.window_manager.show_frame("TestSelectionWindow")).pack(pady=10)
        tk.Button(self, text="Результаты тестирований",
                  command=lambda: master.window_manager.show_frame("ResultsWindow")).pack(pady=10)
        tk.Button(self, text="Отчёты по тестированиям",
                  command=lambda: master.window_manager.show_frame("ReportWindow")).pack(pady=10)

        self.profile_label = tk.Label(self, text="Пользователь: ", font=("Arial", 10))
        self.profile_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def update_data(self, FIO=None, **kwargs):
        if FIO:
            self.profile_label.config(text=f"Пользователь: {FIO}")


# Экран выбора теста
class TestSelectionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Выберите упражнение для тестирования", font=("Arial", 14)).pack(pady=20)

        # Создаем выпадающий список для выбора упражнения
        self.exercise_options = [
            "Взлет",
            "Полет в плохих условиях",
            "Полет в хороших условиях",
            "Посадка"
        ]

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack()

        self.exercise_var = tk.StringVar()
        self.exercise_var.set("Выберете упражнение для тестирования")

        self.exercise_menu = tk.OptionMenu(self, self.exercise_var, *self.exercise_options)
        self.exercise_menu.pack(pady=10)

        self.start_button = tk.Button(self, text="Перейти к тестированию", state=tk.NORMAL,
                                      command=self.start_test)
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.window_manager.show_frame("MainWindow"))
        self.back_button.place(x=10, y=10)

    def start_test(self):
        exercise_var = self.exercise_var.get()
        if exercise_var != "Выберете упражнение для тестирования":
            self.master.window_manager.show_frame("TestInstructionWindow",
                                                  exercise_var=exercise_var,
                                                  current_test="PVT Test")
        else:
            self.error_label.config(text="Выберите упражнение для тестирования")


# Экран с инструкциями к тесту
class TestInstructionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_test = None

        self.instruction_label = tk.Label(self, text="Инструкция к тесту", font=("Arial", 14))
        self.instruction_label.pack(pady=20)

        self.instruction_text = tk.Label(self, text="", wraplength=400, justify="left")
        self.instruction_text.pack(pady=10)

        self.start_test_button = tk.Button(self, text="Начать тест", command=self.start_test)
        self.start_test_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.window_manager.show_frame("TestSelectionWindow"))
        self.back_button.place(x=10, y=10)

    def update_data(self, current_test, **kwargs):
        self.current_test = current_test
        self.instruction_text.config(text=f"Инструкция к {self.current_test}")

    def start_test(self):
        """Метод для начала теста."""
        if self.current_test == "PVT Test":
            self.master.window_manager.show_frame("PVTWindow")
        elif self.current_test == "NASA-TLX Test":
            self.master.window_manager.show_frame("NASA_TLXWindow")
        else:
            tk.Label(self, text="Невозможно начать тест: неизвестный тип", fg="red").pack()


class PVTWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.start_time = None
        self.results = []

        self.label = tk.Label(self, text="Нажмите кнопку, как только увидите сигнал", font=("Arial", 14))
        self.label.pack(pady=20)

        self.button = tk.Button(self, text="Начать тест", command=self.start_test)
        self.button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.window_manager.show_frame("TestSelectionWindow"))
        self.back_button.place(x=10, y=10)

    def start_test(self):
        self.label.config(text="Ожидайте сигнал...")
        self.button.config(state=tk.DISABLED)
        self.master.after(random.randint(2000, 5000), self.show_signal)

    def show_signal(self):
        self.start_time = time.time()
        self.label.config(text="ЖМИ!")
        self.button.config(text="Нажми сейчас!", state=tk.NORMAL, command=self.record_response)

    def record_response(self):
        reaction_time = time.time() - self.start_time
        self.results.append(reaction_time)
        self.label.config(text=f"Ваше время реакции: {reaction_time:.3f} сек")

        if len(self.results) < 2:  # Запускаем тест 5 раз
            self.button.config(text="Следующий раунд", state=tk.NORMAL, command=self.start_test)
        else:
            self.finish_test()

    def finish_test(self):
        avg_reaction = sum(self.results) / len(self.results)
        self.label.config(text=f"Тест завершён! Среднее время реакции: {avg_reaction:.3f} сек")
        self.button.config(text="Завершить", state=tk.NORMAL,
                           command=lambda: self.master.window_manager.show_frame("ExerciseWaitWindow"))

        # Сохраняем результаты теста в базу данных (например)
        self.services.test.save_pvt_results(self.results, avg_reaction)


# Экран ожидания выполнения упражнений на стенде
class ExerciseWaitWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Ожидание выполнения упражнения на стенде", font=("Arial", 14))
        self.label.pack(pady=20)

        self.wait_button = tk.Button(self, text="Далее", command=self.next_stage)
        self.wait_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("PVTWindow"))
        self.back_button.place(x=10, y=10)

    def next_stage(self):
        self.master.window_manager.show_frame("TestInstructionWindow", current_test="NASA-TLX Test")


# Экран для NASA-TLX теста
class NASA_TLXWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.questions = [
            "Какую умственную нагрузку вы ощущали?",
            "Какую физическую нагрузку вы ощущали?",
            "Какую временную нагрузку вы ощущали?",
            "Какую успеваемость вы ощутили?",
            "Какой уровень усилий вы приложили?",
            "Какой уровень стресса вы ощутили?"
        ]
        self.current_question = 0
        self.responses = {}

        self.label = tk.Label(self, text="", font=("Arial", 14), wraplength=400)
        self.label.pack(pady=20)

        self.scale = tk.Scale(self, from_=0, to=20, orient=tk.HORIZONTAL, length=300)
        self.scale.pack(pady=10)

        self.next_button = tk.Button(self, text="Далее", command=self.next_question)
        self.next_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Отменить тест",
                                     command=lambda: master.window_manager.show_frame("MainWindow"))
        self.back_button.place(x=10, y=10)

    def update_data(self, **kwargs):
        self.current_question = 0
        self.responses = {}
        self.display_question()

    def display_question(self):
        if self.current_question < len(self.questions):
            self.label.config(text=self.questions[self.current_question])
            self.scale.set(10)  # Сброс шкалы на среднее значение
        else:
            self.finish_test()

    def next_question(self):
        response = self.scale.get()
        self.responses[self.questions[self.current_question]] = response
        self.current_question += 1
        self.display_question()

    def finish_test(self):
        # Сохраняем результаты NASA-TLX
        # self.services.test.save_nasa_tlx_results(self.responses)
        self.label.config(text="".join(self.responses))

        self.master.window_manager.show_frame("TestCompletionWindow")


# Экран завершения теста
class TestCompletionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Тест завершён. Спасибо за участие!", font=("Arial", 14))
        self.label.pack(pady=20)

        self.finish_button = tk.Button(self, text="Завершить",
                                       command=lambda: master.window_manager.show_frame("MainWindow"))
        self.finish_button.pack(pady=10)
