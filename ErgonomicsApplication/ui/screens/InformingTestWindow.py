# ui/screens/InformingTestWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class InformingTestWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Информация о тестировании",
                 font=("Arial", 24, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        description = (
            "Перед началом тестирования ознакомьтесь с его сутью.\n\n"
            "Тест PVT (Psychomotor Vigilance Test):\n"
            " - Тест на внимание и скорость реакции.\n"
            " - Быстро нажимайте на кнопку при появлении сигнала.\n\n"
            "Тест NASA-TLX (Task Load Index):\n"
            " - Оценка субъективной рабочей нагрузки.\n"
            " - Ответьте на несколько вопросов о восприятии задачи.\n"
        )
        tk.Label(self, text=description, wraplength=600, justify="left",
                 font=("Arial", 12), bg="#f7f7f7", fg="#333").pack(pady=20)

        self.agree_var = tk.BooleanVar()
        tk.Checkbutton(
            self,
            text="Я ознакомлен и готов приступить к тестированию",
            variable=self.agree_var,
            command=self.toggle_button,
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=10)

        self.next_button = tk.Button(
            self,
            text="Перейти к тестам",
            state=tk.DISABLED,
            command=lambda: master.window_manager.show_frame("TestSelectionWindow"),
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.next_button.pack(pady=20)

        tk.Button(
            self,
            text="Назад",
            command=lambda: master.window_manager.show_frame("MainWindow"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        ).place(x=10, y=10)

    def toggle_button(self):
        if self.agree_var.get():
            self.next_button.config(state=tk.NORMAL)
        else:
            self.next_button.config(state=tk.DISABLED)
