import tkinter as tk
from app.database import get_db
from app.services import get_test_results
from app.utils import format_results

class ResultsWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Результаты тестов")
        self.geometry("800x600")

        with next(get_db()) as db:
            results = get_test_results(db)
            formatted_results = format_results(results)

        text = tk.Text(self)
        for result in formatted_results:
            text.insert(tk.END, f"ID: {result['ID']}, Name: {result['Name']}, Test: {result['Test']}, Result: {result['Result']}, Date: {result['Date']}\n")
        text.pack(fill=tk.BOTH, expand=True)
