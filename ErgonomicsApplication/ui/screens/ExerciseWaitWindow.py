# ui/screens/ExerciseWaitWindow.py

import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class ExerciseWaitWindow(CenteredFrame):
    """
    Окно, которое имитирует «выполнение упражнения» (полёт на стенде / тренажёре).
    Пользователь, по идее, переключается в реальное упражнение.
    Мы просто ждём, пока он нажмёт «Далее».
    После этого PVT «после».
    """
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(
            self,
            text="Выполнение упражнения (реальный стенд или имитация).\nНажмите 'Далее', когда закончите.",
            font=("Arial", 14),
            bg="#f7f7f7",
            fg="#333"
        )
        self.label.pack(pady=40)

        self.wait_button = tk.Button(
            self,
            text="Далее (PVT после)",
            command=self.next_stage,
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.wait_button.pack(pady=20)

        self.back_button = tk.Button(
            self,
            text="Назад",
            command=lambda: master.window_manager.show_frame("PVTWindow", type_test="before"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
        self.back_button.place(x=10, y=10)

    def next_stage(self):
        # Теперь запускаем PVT «после»
        self.master.window_manager.show_frame("PVTWindow", type_test="after")
