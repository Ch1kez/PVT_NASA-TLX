import tkinter as tk
import time
import random

from app.services import Services
from ui.components.CenteredFrame import CenteredFrame


class PVTWindow(CenteredFrame):
    """
    Окно для проведения PVT (Psychomotor Vigilance Test).
    Цикл:
    - Несколько раундов (max_rounds).
    - В каждом раунде случайная задержка 2–5 секунд, потом «ЖМИ!».
    - Засекаем время реакции (мс).
    - В конце выводим статистику (среднее, мин, макс).
    - Если type_test='before', это «перед упражнением».
    - Если type_test='after', это «после упражнения».
    """
    def __init__(self, master):
        super().__init__(master)

        self.user_id = None
        self.task_number = None
        self.exercise_name = None
        self.type_test = None       # "before" или "after"
        self.max_rounds = 5        # количество раундов
        self.current_round = 0
        self.results = []          # список времени реакции за каждый раунд (в сек)
        self.start_time = None
        self.services = Services()


        self.label = tk.Label(
            self,
            text="PVT: Нажмите кнопку, как только увидите сигнал",
            font=("Arial", 14),
            bg="#f7f7f7",
            fg="#333"
        )
        self.label.pack(pady=40)

        self.button = tk.Button(
            self,
            text="Начать тест",
            command=self.start_round,
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.button.pack(pady=20)

        # Кнопка «Назад»: возвращается на экран выбора теста
        self.back_button = tk.Button(
            self,
            text="Назад",
            command=lambda: master.window_manager.show_frame("TestSelectionWindow"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
        self.back_button.place(x=10, y=10)

    def update_data(self, type_test: str = "before", exercise_name=None, task_number=None, **kwargs):
        """
        Вызывается при показе экрана.
        Сбрасываем результаты, раунды, выставляем type_test = 'before' или 'after'.
        """
        self.type_test = type_test
        self.exercise_name = exercise_name
        self.task_number = task_number

        self.results.clear()
        self.current_round = 0

        self.label.config(text="PVT: Нажмите кнопку, как только увидите сигнал")
        self.button.config(text="Начать тест", state=tk.NORMAL, command=self.start_round)

    def start_round(self):
        """
        Запускаем очередной раунд (если не достигли max_rounds).
        """
        if self.current_round >= self.max_rounds:
            # Все раунды пройдены - завершаем
            self.finish_test()
            return

        self.label.config(
            text=(
                f"PVT: Раунд {self.current_round + 1} из {self.max_rounds}. "
                "Ожидайте сигнал..."
            )
        )
        self.button.config(state=tk.DISABLED)

        # Случайная задержка 2–5 секунд до появления «ЖМИ!»
        delay_ms = random.randint(2000, 5000)
        self.master.after(delay_ms, self.show_signal)

    def show_signal(self):
        """
        Показываем сигнал "ЖМИ!" и включаем засекание времени.
        """
        self.start_time = time.time()
        self.label.config(text="ЖМИ!")
        self.button.config(text="Нажать сейчас!", state=tk.NORMAL, command=self.record_response)

    def record_response(self):
        """
        Засекаем время реакции, сохраняем и переходим к следующему раунду.
        """
        end_time = time.time()
        reaction_time_s = end_time - self.start_time
        self.results.append(reaction_time_s)

        self.user_id = self.master.window_manager.current_user_id

        self.services.test.save_pvt_round(
            user_id=self.user_id,
            exercise_name=self.exercise_name,
            task_number=self.task_number,
            type_test=self.type_test,
            round_index=self.current_round,
            reaction_time=reaction_time_s
        )

        self.label.config(
            text=f"Время реакции: {reaction_time_s * 1000:.0f} мс"
        )
        self.current_round += 1

        if self.current_round < self.max_rounds:
            self.button.config(text="Следующий раунд", command=self.start_round, state=tk.NORMAL)
        else:
            self.button.config(text="Завершить тест", command=self.finish_test, state=tk.NORMAL)

    def finish_test(self):
        """
        Расчёт итогов: среднее, мин, макс. Переход на следующий экран.
        """
        if len(self.results) == 0:
            avg_ms = 0
            min_ms = 0
            max_ms = 0
        else:
            avg_ms = sum(self.results) / len(self.results) * 1000
            min_ms = min(self.results) * 1000
            max_ms = max(self.results) * 1000

        self.label.config(
            text=(
                f"Тест завершён!\n"
                f"Среднее время: {avg_ms:.0f} мс\n"
                f"Мин. время: {min_ms:.0f} мс\n"
                f"Макс. время: {max_ms:.0f} мс"
            )
        )

        # Кнопка для перехода на «ExerciseWaitWindow» или, если это after, сразу на NASA-TLX
        if self.type_test == "before":
            self.button.config(
                text="Перейти к упражнению",
                command=lambda: self.master.window_manager.show_frame("ExerciseWaitWindow"),
                state=tk.NORMAL
            )
        else:
            self.button.config(
                text="Перейти к NASA-TLX",
                command=lambda: self.master.window_manager.show_frame("TestInstructionWindow", current_test="NASA-TLX Test"),
                state=tk.NORMAL
            )
