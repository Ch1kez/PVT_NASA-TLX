import random
import time
import tkinter as tk
from pydantic import ValidationError
from app.schemas import UserSchema
from app.services import Services as services
from PIL import Image, ImageTk

from app.utils import TestResults

results_store = TestResults()


class CenteredFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)

        self.configure(bg="#f7f7f7")

        # Делает основной контейнер центрированным
        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        # Привязка события изменения размеров окна для корректировки контейнера
        self.bind("<Configure>", self.center_container)

        # Логотипы
        self.left_logo_path = "../GosNIIASLogocolor_removebg_preview.png"
        self.right_logo_path = "../mai_logo.png"

        self.left_logo = ImageTk.PhotoImage(Image.open(self.left_logo_path).resize((80, 80), Image.Resampling.LANCZOS))
        self.right_logo = ImageTk.PhotoImage(Image.open(self.right_logo_path).resize((80, 80), Image.Resampling.LANCZOS))

        # Левый логотип
        self.left_logo_label = tk.Label(self, image=self.left_logo, bg="#f7f7f7")
        self.left_logo_label.place(relx=1.0, x=-10, y=10, anchor="ne")

        # Правый логотип
        self.right_logo_label = tk.Label(self, image=self.right_logo, bg="#f7f7f7")
        self.right_logo_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    def center_container(self, event=None):
        """Перемещает контейнер в центр окна при изменении размеров."""
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def add_to_container(self, widget):
        """Добавляет виджет в контейнер для удобства."""
        widget.pack(pady=10)


class AuthWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Добро пожаловать!", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)

        login_button = tk.Button(self, text="Вход", font=("Arial", 14), bg="#0047ab", fg="white",
                                 activebackground="#0051c7", activeforeground="white",
                                 command=lambda: master.window_manager.show_frame("LoginWindow"))
        login_button.pack(pady=10)

        register_button = tk.Button(self, text="Зарегистрироваться", font=("Arial", 14), bg="#0047ab", fg="white",
                                     activebackground="#0051c7", activeforeground="white",
                                     command=lambda: master.window_manager.show_frame("RegisterWindow"))
        register_button.pack(pady=10)

        tk.Label(self, text="© 2024, Ваша компания", bg="#f7f7f7", fg="#555").pack(side="bottom", pady=10)


class RegisterWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.services = services
        self.configure(bg="#f7f7f7")  # светло-серый фон

        # Заголовок
        tk.Label(self, text="Регистрация", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=20)

        # Поля ввода
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

        # Ошибки и кнопки
        self.error_label = tk.Label(self, text="", fg="red", bg="#f7f7f7", font=("Arial", 12))
        self.error_label.pack(pady=10)

        self.register_button = tk.Button(self, text="Регистрация", font=("Arial", 14), bg="#0047ab", fg="white",
                                         activebackground="#0051c7", activeforeground="white", command=self.register)
        self.register_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад", font=("Arial", 14), bg="#0047ab", fg="white",
                                     activebackground="#0051c7", activeforeground="white",
                                     command=lambda: master.window_manager.show_frame("AuthWindow"))
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


class LoginWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        # Заголовок окна
        tk.Label(self, text="Вход", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        # Поле для имени пользователя
        tk.Label(self, text="Имя пользователя:", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack(pady=5)
        self.username_entry = tk.Entry(self, font=("Arial", 14))
        self.username_entry.pack(pady=10, padx=20)

        # Поле для пароля
        tk.Label(self, text="Пароль:", font=("Arial", 14), bg="#f7f7f7", fg="#333").pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 14), show="*")
        self.password_entry.pack(pady=10, padx=20)

        # Кнопка входа
        login_button = tk.Button(self, text="Войти", font=("Arial", 14), bg="#0047ab", fg="white",
                                 activebackground="#0051c7", activeforeground="white", command=self.login)
        login_button.pack(pady=20)

        # Кнопка назад
        back_button = tk.Button(self, text="Назад", font=("Arial", 12), bg="#f7f7f7", fg="#0047ab",
                                activebackground="#f1f1f1", activeforeground="#0047ab",
                                command=lambda: master.window_manager.show_frame("AuthWindow"))
        back_button.place(x=10, y=10)

        # Ошибка
        self.error_label = tk.Label(self, text="", fg="red", bg="#f7f7f7", font=("Arial", 12))
        self.error_label.pack(pady=10)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        FIO = services.user.check_user(login=username, password=password)

        # Переход на главную страницу или вывод ошибки
        if FIO:
            self.master.window_manager.show_frame("MainWindow", FIO=FIO)
        else:
            self.error_label.config(text="Неверный логин или пароль!")


# Главное меню
class MainWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        # Заголовок окна
        tk.Label(self, text="Эргономическая оценка кабины самолета", font=("Arial", 20, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        # Кнопка "Перейти к тестированию"
        test_button = tk.Button(self, text="Перейти к тестированию", font=("Arial", 14), bg="#0047ab", fg="white",
                                activebackground="#0051c7", activeforeground="white",
                                command=lambda: master.window_manager.show_frame("InformingTestWindow"))
        test_button.pack(pady=10)

        # Кнопка "Результаты тестирований"
        results_button = tk.Button(self, text="Результаты тестирований", font=("Arial", 14), bg="#0047ab", fg="white",
                                   activebackground="#0051c7", activeforeground="white",
                                   command=lambda: master.window_manager.show_frame("ResultsWindow"))
        results_button.pack(pady=10)

        # Кнопка "Отчёты по тестированиям"
        reports_button = tk.Button(self, text="Отчёты по тестированиям", font=("Arial", 14), bg="#0047ab", fg="white",
                                   activebackground="#0051c7", activeforeground="white",
                                   command=lambda: master.window_manager.show_frame("ReportWindow"))
        reports_button.pack(pady=10)

        # Метка с информацией о пользователе
        self.profile_label = tk.Label(self, text="Пользователь: ", font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.profile_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def update_data(self, FIO=None, **kwargs):
        if FIO:
            self.profile_label.config(text=f"Пользователь: {FIO}")


# Экран с информацией о тестировании
class InformingTestWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        # Заголовок окна
        tk.Label(self, text="Информация о тестировании", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        # Описание тестирования
        description = (
            "Перед началом тестирования ознакомьтесь с его сутью.\n\n"
            "Тест PVT (Psychomotor Vigilance Test):\n"
            "Тест на внимание и скорость реакции. В течение нескольких раундов вы будете "
            "должны как можно быстрее нажимать на кнопку, когда увидите сигнал. Результаты покажут вашу "
            "среднюю скорость реакции и вариативность.\n\n"
            "Тест NASA-TLX (Task Load Index):\n"
            "Методика оценки субъективной рабочей нагрузки. Вы ответите на несколько вопросов, касающихся "
            "вашего восприятия умственной, физической и временной нагрузки, а также стресса и усилий. "
            "Эти данные помогут оценить эргономические условия выполнения задачи."
        )
        tk.Label(self, text=description, wraplength=600, justify="left", font=("Arial", 12), bg="#f7f7f7", fg="#333").pack(pady=20)

        # Добавление галочки для подтверждения согласия
        self.agree_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Я ознакомлен и готов приступить к тестированию",
                       variable=self.agree_var, command=self.toggle_button, font=("Arial", 12), bg="#f7f7f7", fg="#333").pack(pady=10)

        # Кнопка для перехода дальше
        self.next_button = tk.Button(self, text="Перейти к тестам", state=tk.DISABLED,
                                     command=lambda: master.window_manager.show_frame("TestSelectionWindow"), font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.next_button.pack(pady=20)

        # Кнопка "Назад"
        tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("MainWindow"), font=("Arial", 12), bg="#f7f7f7", fg="#333").place(x=10, y=10)

    def toggle_button(self):
        """Активирует или деактивирует кнопку в зависимости от состояния галочки."""
        if self.agree_var.get():
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)


# Экран выбора теста
class TestSelectionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Выберите упражнение для тестирования", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        # Создаем выпадающий список для выбора упражнения
        self.exercise_options = [
            "Взлет",
            "Полет в плохих условиях",
            "Полет в хороших условиях",
            "Посадка"
        ]

        self.task_options = [
            "1",
            "2",
            "3",
            "3"
        ]

        self.error_label = tk.Label(self, text="", fg="red", font=("Arial", 12))
        self.error_label.pack()

        self.exercise_var = tk.StringVar()
        self.exercise_var.set("Выберете упражнение")

        self.task_var = tk.StringVar()
        self.task_var.set("Выберете номер задачи")

        self.exercise_menu = tk.OptionMenu(self, self.exercise_var, *self.exercise_options)
        self.exercise_menu.config(font=("Arial", 12))
        self.exercise_menu.pack(pady=10)

        self.task_menu = tk.OptionMenu(self, self.task_var, *self.task_options)
        self.task_menu.config(font=("Arial", 12))
        self.task_menu.pack(pady=10)

        self.start_button = tk.Button(self, text="Перейти к тестированию", state=tk.NORMAL,
                                      command=self.start_test, font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.window_manager.show_frame("MainWindow"), font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.back_button.place(x=10, y=10)

    def start_test(self):
        exercise_var = self.exercise_var.get()
        task_var = self.task_var.get()

        self.error_label.config(text="")

        if exercise_var == "Выберете упражнение":
            self.error_label.config(text="Выберите упражнение для тестирования")
            return

        if task_var == "Выберете номер задачи":
            self.error_label.config(text="Выберите номер задачи")
            return

        self.master.window_manager.show_frame(
            "TestInstructionWindow",
            exercise_var=exercise_var,
            current_test="PVT Test"
        )


# Экран с инструкциями к тесту
class TestInstructionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.current_test = None

        # Заголовок окна
        self.instruction_label = tk.Label(self, text="Инструкция к тесту", font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333")
        self.instruction_label.pack(pady=40)

        # Поле для текста инструкции
        self.instruction_text = tk.Label(self, text="", wraplength=500, justify="left", font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.instruction_text.pack(pady=20)

        # Кнопка для начала теста
        self.start_test_button = tk.Button(self, text="Начать тест", command=self.start_test, state=tk.DISABLED, font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.start_test_button.pack(pady=20)

        # Добавление галочки для подтверждения готовности
        self.ready_var = tk.BooleanVar()
        tk.Checkbutton(self, text="Я ознакомлен с инструкцией и готов приступить", variable=self.ready_var, command=self.toggle_start_button, font=("Arial", 12), bg="#f7f7f7", fg="#333").pack()

        # Кнопка "Назад"
        self.back_button = tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("TestSelectionWindow"), font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.back_button.place(x=10, y=10)

    def update_data(self, current_test=None, **kwargs):
        """Обновляет данные и показывает соответствующую инструкцию."""
        self.current_test = current_test

        if current_test == "PVT Test":
            instruction = (
                "### Тест PVT (Psychomotor Vigilance Test)\n\n"
                "Цель: Проверка вашей способности быстро реагировать на визуальный сигнал.\n\n"
                "Процедура:\n"
                "- Когда на экране появится сигнал (слово «ЖМИ!»), нажмите на кнопку как можно быстрее.\n"
                "- Тест состоит из нескольких раундов, результаты фиксируют время вашей реакции.\n\n"
                "Польза: Этот тест позволяет оценить вашу внимательность и уровень усталости.\n"
            )
        elif current_test == "NASA-TLX Test":
            instruction = (
                "### Тест NASA-TLX (Task Load Index)\n\n"
                "Цель: Оценить субъективную рабочую нагрузку при выполнении задачи.\n\n"
                "Процедура:\n"
                "- Вам нужно будет ответить на 6 вопросов, оценив каждый параметр нагрузки по шкале от 0 до 20.\n"
                "- Вопросы касаются вашего восприятия умственной, физической и временной нагрузки, "
                "усилий, стресса и эффективности выполнения.\n\n"
                "Польза: Результаты покажут, насколько сложной и напряжённой была задача для вас.\n"
            )
        else:
            instruction = "Инструкция для данного теста недоступна."

        self.instruction_text.config(text=instruction, )
        self.start_test_button.config(state=tk.DISABLED)  # Отключаем кнопку, пока галочка не будет нажата.

    def toggle_start_button(self):
        """Активирует или деактивирует кнопку в зависимости от состояния галочки."""
        if self.ready_var.get():
            self.start_test_button.config(state=tk.NORMAL)
        else:
            self.start_test_button.config(state=tk.DISABLED)

    def start_test(self):
        """Метод для начала теста."""
        if self.current_test == "PVT Test":
            self.master.window_manager.show_frame("PVTWindow", type_test="before")
        elif self.current_test == "NASA-TLX Test":
            self.master.window_manager.show_frame("NASA_TLXWindow")


# Экран PVT
class PVTWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.type_test = None
        self.results = []
        self.start_time = None
        self.results_store = results_store

        self.label = tk.Label(self, text="Нажмите кнопку, как только увидите сигнал", font=("Arial", 14), bg="#f7f7f7", fg="#333")
        self.label.pack(pady=40)

        self.button = tk.Button(self, text="Начать тест", command=self.start_test, font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.button.pack(pady=20)

        self.back_button = tk.Button(self, text="Назад", command=lambda: master.window_manager.show_frame("TestSelectionWindow"), font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.back_button.place(x=10, y=10)

    def update_data(self, type_test: str, **kwargs):
        if type_test:
            self.type_test = type_test

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

        if self.type_test == "after":
            self.results_store.add_pvt_after(reaction_time)  # Сохраняем результат после теста PVT
        else:
            self.results_store.add_pvt_before(reaction_time)  # Сохраняем результат перед тестом PVT

        self.label.config(text=f"Ваше время реакции: {reaction_time:.3f} сек")

        if len(self.results) < 2:  # Запускаем тест 5 раз
            self.button.config(text="Следующий раунд", state=tk.NORMAL, command=self.start_test)
        else:
            self.finish_test()

    def finish_test(self):
        avg_reaction = sum(self.results) / len(self.results)
        self.label.config(text=f"Тест завершён! Среднее время реакции: {avg_reaction:.3f} сек")
        self.button.config(text="Завершить", state=tk.NORMAL, command=lambda: self.master.window_manager.show_frame("ExerciseWaitWindow"))

        # Сохраняем результаты теста
        print(self.results, avg_reaction)


# Экран ожидания выполнения упражнения на стенде
class ExerciseWaitWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(self, text="Ожидание выполнения упражнения на стенде",
                              font=("Arial", 14), bg="#f7f7f7", fg="#333")
        self.label.pack(pady=40)

        self.wait_button = tk.Button(self, text="Далее",
                                     command=self.next_stage, font=("Arial", 14), bg="#0047ab", fg="white",
                                     activebackground="#0051c7", activeforeground="white")
        self.wait_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Назад",
                                     command=lambda: master.window_manager.show_frame("PVTWindow", type_test="after"),
                                     font=("Arial", 12), bg="#f7f7f7", fg="#333")
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
        self.results_store = results_store

        self.label = tk.Label(self, text="", font=("Arial", 14), wraplength=400, bg="#f7f7f7", fg="#333")
        self.label.pack(pady=40)

        self.scale = tk.Scale(self, from_=0, to=20, orient=tk.HORIZONTAL, length=300, font=("Arial", 12))
        self.scale.pack(pady=20)

        self.next_button = tk.Button(self, text="Далее", command=self.next_question, font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.next_button.pack(pady=20)

        self.back_button = tk.Button(self, text="Отменить тест", command=lambda: master.window_manager.show_frame("MainWindow"), font=("Arial", 12), bg="#f7f7f7", fg="#333")
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
        for question, response in self.responses.items():
            self.results_store.add_nasa_tlx(question, response)  # Сохраняем результаты NASA-TLX
        self.label.config(text="Тест завершён! Ваши результаты сохранены.")
        self.master.window_manager.show_frame("TestCompletionWindow")


# Экран завершения теста
class TestCompletionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.results_store = results_store

        # Выводим итоговые результаты
        result_text = self.results_store.get_summary()
        self.label = tk.Label(self, text="Тест завершён. Спасибо за участие!\n\n" + result_text, font=("Arial", 14), bg="#f7f7f7", fg="#333", justify="left")
        self.label.pack(pady=40)

        # Кнопка завершения
        self.finish_button = tk.Button(self, text="Завершить", command=lambda: master.window_manager.show_frame("MainWindow"), font=("Arial", 14), bg="#0047ab", fg="white", activebackground="#0051c7", activeforeground="white")
        self.finish_button.pack(pady=20)
