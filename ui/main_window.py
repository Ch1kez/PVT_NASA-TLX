import tkinter as tk
from ui.pvt_window import PVTWindow
from ui.nasa_tlx_window import NASA_TLXWindow
from ui.results_window import ResultsWindow

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Эргономическая оценка кабины самолета")
        self.geometry("800x600")

        tk.Label(self, text="Добро пожаловать!", font=("Arial", 16)).pack(pady=20)

        tk.Button(self, text="Пройти PVT тест", command=self.open_pvt).pack(pady=10)
        tk.Button(self, text="Пройти NASA-TLX тест", command=self.open_nasa_tlx).pack(pady=10)
        tk.Button(self, text="Результаты тестов", command=self.open_results).pack(pady=10)

    def open_pvt(self):
        PVTWindow(self)

    def open_nasa_tlx(self):
        NASA_TLXWindow(self)

    def open_results(self):
        ResultsWindow(self)
