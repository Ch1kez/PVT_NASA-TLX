from tkinter import Tk

from app.database import init_db
from ui.window_manager import WindowManager
from ui.screens import AuthWindow, LoginWindow, RegisterWindow, MainWindow, PVTWindow, NASA_TLXWindow, ResultsWindow, ReportWindow

def main():

    init_db()

    root = Tk()
    root.geometry("800x600")
    root.title("Эргономическая оценка кабины самолета")

    # Создаем менеджер окон
    window_manager = WindowManager(root)
    root.window_manager = window_manager

    # Регистрируем все кадры
    window_manager.create_and_register("AuthWindow", AuthWindow)
    window_manager.create_and_register("LoginWindow", LoginWindow)
    window_manager.create_and_register("RegisterWindow", RegisterWindow)
    window_manager.create_and_register("MainWindow", MainWindow)
    window_manager.create_and_register("PVTWindow", PVTWindow)
    window_manager.create_and_register("NASA_TLXWindow", NASA_TLXWindow)
    window_manager.create_and_register("ResultsWindow", ResultsWindow)
    window_manager.create_and_register("ReportWindow", ReportWindow)

    # Показ начального экрана
    window_manager.show_frame("AuthWindow")

    root.mainloop()

if __name__ == "__main__":
    main()
