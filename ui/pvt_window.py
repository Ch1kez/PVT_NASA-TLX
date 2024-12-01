import tkinter as tk
import random
import time


class PVTWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Тест PVT")
        self.geometry("400x200")
        self.label = tk.Label(self, text="Нажмите 'СТАРТ', чтобы начать тест.", font=("Arial", 14))
        self.label.pack(pady=20)

        self.start_button = tk.Button(self, text="СТАРТ", command=self.start_test)
        self.start_button.pack(pady=10)

        self.react_button = tk.Button(self, text="РЕАГИРУЙТЕ", state=tk.DISABLED, command=self.record_reaction_time)
        self.react_button.pack(pady=10)

        self.start_time = None  # Время начала реакции

    def start_test(self):
        self.start_button.config(state=tk.DISABLED)
        self.react_button.config(state=tk.DISABLED)
        self.label.config(text="Подождите...")
        self.update()

        delay = random.uniform(2, 5)  # Случайная задержка
        self.after(int(delay * 1000), self.enable_reaction_phase)  # Запуск реакции через задержку

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
