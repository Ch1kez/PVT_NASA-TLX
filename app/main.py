from ui.main_window import MainWindow
from ui.auth_window import AuthWindow
from app.database import init_db

if __name__ == "__main__":
    init_db()
    app = AuthWindow()
    app.mainloop()
