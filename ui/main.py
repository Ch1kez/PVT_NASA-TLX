from tkinter import Tk
from app.database import init_db
from ui.window_manager import WindowManager
from ui.screens import (
    AuthWindow, LoginWindow, RegisterWindow, MainWindow,
    TestSelectionWindow, TestInstructionWindow,
    TestCompletionWindow, PVTWindow, NASA_TLXWindow, ExerciseWaitWindow
)

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
    root.geometry("800x600")  # Можно сделать динамическим через root.resizable(True, True)
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
