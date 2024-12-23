# ui/screens/TestCompletionWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame

class TestCompletionWindow(CenteredFrame):
    """
    Завершающее окно. Здесь мы можем вывести итоги,
    но пока просто спасибо и кнопка возврата.
    """
    def __init__(self, master):
        super().__init__(master)
        self.label = tk.Label(
            self,
            text="Все тесты завершены! Спасибо за участие.",
            font=("Arial", 16),
            bg="#f7f7f7",
            fg="#333"
        )
        self.label.pack(pady=40)

        finish_button = tk.Button(
            self,
            text="На главную",
            command=lambda: master.window_manager.show_frame("MainWindow"),
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        finish_button.pack(pady=20)
