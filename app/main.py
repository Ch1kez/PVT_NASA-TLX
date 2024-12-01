from ui.main_window import MainWindow
from app.database import init_db

if __name__ == "__main__":
    init_db()
    app = MainWindow()
    app.mainloop()
