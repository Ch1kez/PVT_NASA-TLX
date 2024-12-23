import tkinter as tk
from tkinter import messagebox
import sqlite3

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('aviation_ergonomics.db')
    cursor = conn.cursor()
    # Создаем таблицы
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        experiment_id INTEGER NOT NULL
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS PVTResults (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        reaction_time REAL,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )""")
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS NASA_TLX (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        mental_demand INTEGER,
        physical_demand INTEGER,
        temporal_demand INTEGER,
        performance INTEGER,
        effort INTEGER,
        frustration INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users (id)
    )""")
    conn.commit()
    conn.close()

# Запуск интерфейса
def main_menu():
    root = tk.Tk()
    root.title("Эргономическая оценка кабины самолета")

    def open_pvt_test():
        messagebox.showinfo("PVT Test", "Открывается тест PVT")

    def open_nasa_tlx():
        messagebox.showinfo("NASA-TLX", "Открывается NASA-TLX")

    tk.Label(root, text="Выберите действие").pack()
    tk.Button(root, text="Тест PVT", command=open_pvt_test).pack(pady=5)
    tk.Button(root, text="Оценка NASA-TLX", command=open_nasa_tlx).pack(pady=5)

    root.mainloop()

if __name__ == "__main__":
    init_db()
    main_menu()
