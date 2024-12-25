# ui/screens/MainWindow.py
import tkinter as tk
from ui.components.CenteredFrame import CenteredFrame


class MainWindow(CenteredFrame):
    def __init__(self, master):
        super().__init__(master)

        tk.Label(self, text="Эргономическая оценка кабины самолета",
                 font=("Arial", 20, "bold"), bg="#f7f7f7", fg="#333").pack(pady=40)

        test_button = tk.Button(
            self,
            text="Перейти к тестированию",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: master.window_manager.show_frame("InformingTestWindow")
        )
        test_button.pack(pady=10)

        results_button = tk.Button(
            self,
            text="Результаты тестирований",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: print("Переход к результатам (не реализовано)")
        )
        results_button.pack(pady=10)

        reports_button = tk.Button(
            self,
            text="Отчёты по тестированиям",
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white",
            command=lambda: print("Переход к отчетам (не реализовано)")
        )
        reports_button.pack(pady=10)

        logout_button = tk.Button(
            self,
            text="Выйти",
            command=self.logout,
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
        logout_button.place(x=10, y=10)

        self.profile_label = tk.Label(self, text="Пользователь: ", font=("Arial", 12), bg="#f7f7f7", fg="#333")
        self.profile_label.place(relx=0.0, rely=1.0, anchor="sw", x=10, y=-10)

    def update_data(self, FIO=None, **kwargs):
        if FIO:
            self.profile_label.config(text=f"Пользователь: {FIO}")

    def logout(self):
        self.master.window_manager.current_user_id = None
        self.master.window_manager.show_frame("AuthWindow")
