# app.py
from tkinter import Tk
from app.database.database import init_db
from ui.window_manager import WindowManager
from ui.screens import AuthWindow
from ui.screens.LoginWindow import LoginWindow
from ui.screens.RegisterWindow import RegisterWindow
from ui.screens.MainWindow import MainWindow
from ui.screens.TestSelectionWindow import TestSelectionWindow
from ui.screens.TestInstructionWindow import TestInstructionWindow
from ui.screens.TestCompletionWindow import TestCompletionWindow
from ui.screens.PVTWindow import PVTWindow
from ui.screens.NASA_TLXWindow import NASA_TLXWindow
from ui.screens.ExerciseWaitWindow import ExerciseWaitWindow
from ui.screens.InformingTestWindow import InformingTestWindow

def register_frames(window_manager):
    """Регистрируем все окна приложения в менеджере окон."""
    frames = {
        "AuthWindow": AuthWindow,
        "LoginWindow": LoginWindow,
        "RegisterWindow": RegisterWindow,
        "MainWindow": MainWindow,
        "TestSelectionWindow": TestSelectionWindow,
        "TestInstructionWindow": TestInstructionWindow,
        "TestCompletionWindow": TestCompletionWindow,
        "PVTWindow": PVTWindow,
        "NASA_TLXWindow": NASA_TLXWindow,
        "ExerciseWaitWindow": ExerciseWaitWindow,
        "InformingTestWindow": InformingTestWindow
    }

    for frame_name, frame_class in frames.items():
        window_manager.create_and_register(frame_name, frame_class)

def main():
    """Главная функция для запуска приложения."""
    # Инициализация базы данных
    try:
        init_db()
        print("База данных успешно инициализирована.")
    except Exception as e:
        print(f"Ошибка при инициализации базы данных: {e}")
        return

    # Создаем основное окно приложения
    root = Tk()
    root.geometry("800x600")
    root.title("Эргономическая оценка кабины самолета")

    # Создаем менеджер окон
    window_manager = WindowManager(root)
    root.window_manager = window_manager

    # Регистрируем все окна приложения
    register_frames(window_manager)

    # Показ начального экрана
    window_manager.show_frame("AuthWindow")

    # Запуск основного цикла приложения
    root.mainloop()

if __name__ == "__main__":
    main()
