# ui/screens/TestSelectionWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class TestSelectionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        tk.Label(self, text="Выберите упражнение для тестирования",
                 font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

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

        self.start_button = tk.Button(
            self,
            text="Перейти к тестированию",
            state=tk.NORMAL,
            command=self.start_test,
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.start_button.pack(pady=10)

        self.back_button = tk.Button(
            self,
            text="Назад",
            command=lambda: master.window_manager.show_frame("MainWindow"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
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
            task_number=task_var,
            current_test="PVT Test"
        )
