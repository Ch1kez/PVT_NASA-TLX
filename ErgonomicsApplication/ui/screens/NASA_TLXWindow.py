# ui/screens/NASA_TLXWindow.py
import tkinter as tk

from app.services import Services
from ui.components.CenteredFrame import CenteredFrame

class NASA_TLXWindow(CenteredFrame):
    """
    Окно NASA-TLX с 2 шагами:
    1) Оценка по 6 шкалам (0–100).
    2) 15 парных сравнений для определения весов.
    3) Итоговый расчёт Weighted TLX.

    Шкалы:
    - mental_demand
    - physical_demand
    - temporal_demand
    - performance
    - effort
    - frustration
    """
    def __init__(self, master):
        super().__init__(master)

        self.services = Services()

        self.exercise_name = None
        self.task_number = None
        self.user_id = None

        self.step = 0  # 0=шкалы, 1=парные сравнения, 2=конец
        self.questions = [
            "Mental Demand (Умственная нагрузка)",
            "Physical Demand (Физическая нагрузка)",
            "Temporal Demand (Временная нагрузка)",
            "Performance (Удовлетворённость выполнением)",
            "Effort (Общие усилия)",
            "Frustration (Уровень фрустрации)"
        ]
        # Храним оценки (0..100)
        self.scores = [0, 0, 0, 0, 0, 0]
        self.current_question = 0

        # Для шкал
        self.label_question = tk.Label(self, text="", font=("Arial", 14), wraplength=400, bg="#f7f7f7", fg="#333")
        self.label_question.pack(pady=20)

        self.scale = tk.Scale(self, from_=0, to=100, orient=tk.HORIZONTAL, length=300, font=("Arial", 12))
        self.scale.pack(pady=10)

        self.next_button = tk.Button(
            self,
            text="Далее",
            command=self.next_action,
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        self.next_button.pack(pady=20)

        self.back_button = tk.Button(
            self,
            text="Отменить тест",
            command=lambda: master.window_manager.show_frame("MainWindow"),
            font=("Arial", 12),
            bg="#f7f7f7",
            fg="#333"
        )
        self.back_button.place(x=10, y=10)

        # Структуры для «весов»
        self.all_pairs = [
            ("Mental", "Physical"), ("Mental", "Temporal"), ("Mental", "Performance"), ("Mental", "Effort"), ("Mental", "Frustration"),
            ("Physical", "Temporal"), ("Physical", "Performance"), ("Physical", "Effort"), ("Physical", "Frustration"),
            ("Temporal", "Performance"), ("Temporal", "Effort"), ("Temporal", "Frustration"),
            ("Performance", "Effort"), ("Performance", "Frustration"),
            ("Effort", "Frustration")
        ]
        # Привязка названий к индексам
        self.name_to_index = {
            "Mental": 0,
            "Physical": 1,
            "Temporal": 2,
            "Performance": 3,
            "Effort": 4,
            "Frustration": 5
        }
        # Сколько раз каждая шкала выиграла
        self.weights = [0, 0, 0, 0, 0, 0]  # соответствует 6 шкалам

        # Для парных сравнений
        self.pair_index = 0
        self.label_pair = tk.Label(self, text="", font=("Arial", 14), bg="#f7f7f7", fg="#333")
        # Кнопки сравнения
        self.button_left = tk.Button(self, text="", font=("Arial", 12), command=self.choose_left)
        self.button_right = tk.Button(self, text="", font=("Arial", 12), command=self.choose_right)

    def update_data(self, exercise_var=None, task_number=None, user_id=None, **kwargs):
        """
        Сбрасываем всё при входе на экран.
        """
        self.exercise_name = exercise_var
        self.task_number = task_number
        self.user_id = user_id

        self.step = 0
        self.current_question = 0
        self.pair_index = 0
        self.weights = [0, 0, 0, 0, 0, 0]
        self.scores = [0, 0, 0, 0, 0, 0]

        self.show_question_step()

    def show_question_step(self):
        """
        Шаг 1: Показываем вопрос из списка self.questions[self.current_question].
        """
        if self.current_question < len(self.questions):
            self.label_question.config(text=f"{self.questions[self.current_question]}\n(0=минимум, 100=максимум)")
            self.scale.set(50)  # Среднее значение
        else:
            # Переходим к парным сравнениям
            self.step = 1
            self.show_pairs_step()

    def next_action(self):
        """
        Универсальная кнопка "Далее".
        Если step=0, мы собираем шкалы.
        Если step=1, парные сравнения.
        """
        if self.step == 0:
            self.save_current_score()
        elif self.step == 1:
            # Если мы на шаге парных сравнений - ничего не делаем в next_button (т.к. у нас кнопки Left/Right)
            pass

    def save_current_score(self):
        response = self.scale.get()
        self.scores[self.current_question] = response
        self.current_question += 1
        if self.current_question < len(self.questions):
            self.show_question_step()
        else:
            # Закончили шкалы
            self.show_pairs_step()

    def show_pairs_step(self):
        """
        Переходим ко 2-му шагу (парные сравнения).
        Прячем виджеты для шкал, показываем виджеты для сравнения.
        """
        self.step = 1
        self.label_question.pack_forget()
        self.scale.pack_forget()
        self.next_button.pack_forget()

        self.label_pair.pack(pady=20)
        self.button_left.pack(side="left", padx=50)
        self.button_right.pack(side="right", padx=50)

        self.show_next_pair()

    def show_next_pair(self):
        """
        Показываем пару. Например, ("Mental", "Physical").
        """
        if self.pair_index >= len(self.all_pairs):
            # Все пары сравнили
            self.finish_weighting()
            return

        left_name, right_name = self.all_pairs[self.pair_index]
        self.label_pair.config(text=f"Что было важнее?\n{left_name} vs {right_name}")
        self.button_left.config(text=left_name)
        self.button_right.config(text=right_name)

    def choose_left(self):
        """
        Если пользователь выбрал левую шкалу, увеличиваем её вес.
        """
        left_name, _ = self.all_pairs[self.pair_index]
        idx = self.name_to_index[left_name]
        self.weights[idx] += 1

        self.pair_index += 1
        self.show_next_pair()

    def choose_right(self):
        """
        Если пользователь выбрал правую шкалу, увеличиваем её вес.
        """
        _, right_name = self.all_pairs[self.pair_index]
        idx = self.name_to_index[right_name]
        self.weights[idx] += 1

        self.pair_index += 1
        self.show_next_pair()

    def finish_weighting(self):
        """
        Завершаем парные сравнения.
        Переходим к подсчёту Weighted NASA-TLX.
        """
        self.step = 2
        self.label_pair.config(text="Идёт подсчёт результатов...")

        # Прячем кнопки
        self.button_left.pack_forget()
        self.button_right.pack_forget()

        self.calculate_tlx()

    def calculate_tlx(self):
        """
        Считаем Weighted TLX:
        Weighted_TLX = sum(Score_i * Weight_i) / sum(Weight_i)
        Если все Weight_i=0 (например, пользователь что-то не выбрал?), делим на 1.
        """
        total_weight = sum(self.weights)
        if total_weight == 0:
            total_weight = 1  # чтобы не было деления на ноль

        weighted_sum = 0
        for i, score_value in enumerate(self.scores):
            weighted_sum += score_value * self.weights[i]

        weighted_tlx = weighted_sum / total_weight

        self.user_id = self.master.window_manager.current_user_id

        self.services.test.save_nasa_tlx_result(
            user_id=self.user_id,
            exercise_name=self.exercise_name or "Unknown",
            task_number=self.task_number or "0",
            mental_demand=self.scores[0],
            physical_demand=self.scores[1],
            temporal_demand=self.scores[2],
            performance=self.scores[3],
            effort=self.scores[4],
            frustration=self.scores[5],
            weight_mental=self.weights[0],
            weight_physical=self.weights[1],
            weight_temporal=self.weights[2],
            weight_performance=self.weights[3],
            weight_effort=self.weights[4],
            weight_frustration=self.weights[5],
            weighted_tlx=weighted_tlx
        )

        text_result = (
            "Результаты NASA-TLX:\n\n"
            f"Ваши оценки (0-100) по шкалам:\n"
            f"Mental: {self.scores[0]}, Physical: {self.scores[1]}, Temporal: {self.scores[2]},\n"
            f"Performance: {self.scores[3]}, Effort: {self.scores[4]}, Frustration: {self.scores[5]}\n\n"
            f"Вес каждой шкалы (0..5): {self.weights}\n\n"
            f"Итоговый Weighted TLX = {weighted_tlx:.1f} (из 100)\n"
        )

        self.label_pair.config(text=text_result)

        # Кнопка завершения
        finish_btn = tk.Button(
            self,
            text="Завершить",
            command=lambda: self.master.window_manager.show_frame("TestCompletionWindow"),
            font=("Arial", 14),
            bg="#0047ab",
            fg="white",
            activebackground="#0051c7",
            activeforeground="white"
        )
        finish_btn.pack(pady=30)
