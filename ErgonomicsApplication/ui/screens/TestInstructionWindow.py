# ui/screens/TestInstructionWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class TestInstructionWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)
        self.task_number = None
        self.exercise_name = None
        self.current_test = None

        self.instruction_label = tk.Label(self, text="Инструкция к тесту",
                                          font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333")
        self.instruction_label.pack(pady=40)

        self.instruction_text = tk.Label(self, text="", wraplength=500,
                                         justify="left", font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.instruction_text.pack(pady=20)

        self.start_test_button = tk.Button(
            self,
            text="Начать тест",
            command=self.start_test,
            state=tk.DISABLED,
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.start_test_button.pack(pady=20)

        self.ready_var = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Я ознакомлен с инструкцией и готов приступить",
            variable=self.ready_var,
            command=self.toggle_start_button,
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        ).pack()

        self.back_button = tk.Button(
            self,
            text="Назад",
            command=lambda: master.window_manager.show_frame("TestSelectionWindow"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
        self.back_button.place(x=10, y=10)

    def update_data(self, current_test=None, exercise_var=None, task_number=None, **kwargs):
        self.current_test = current_test
        self.exercise_name = exercise_var
        self.task_number = task_number

        if current_test == "PVT Test":
            instruction = (
                "### Тест PVT (Psychomotor Vigilance Test)\n\n"
                "1) Ждите сигнала на экране.\n"
                "2) При появлении слова «ЖМИ!» — нажмите на кнопку.\n"
                "3) Тест измеряет вашу скорость реакции.\n\n"
            )
        elif current_test == "NASA-TLX Test":
            instruction = (
                "### Тест NASA-TLX (Task Load Index)\n\n"
                "Оцените субъективную нагрузку по 6 шкалам...\n"
            )
        else:
            instruction = "Инструкция для данного теста недоступна."

        self.instruction_text.config(text=instruction)
        self.start_test_button.config(state=tk.DISABLED)

    def toggle_start_button(self):
        if self.ready_var.get():
            self.start_test_button.config(state=tk.NORMAL)
        else:
            self.start_test_button.config(state=tk.DISABLED)

    def start_test(self):
        if self.current_test == "PVT Test":
            self.master.window_manager.show_frame(
                "PVTWindow",
                type_test="before",
                exercise_name=self.exercise_name,
                task_number=self.task_number
            )
        elif self.current_test == "NASA-TLX Test":
            self.master.window_manager.show_frame("NASA_TLXWindow")
