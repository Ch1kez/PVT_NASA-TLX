import tkinter as tk
from PIL import Image, ImageTk


class CenteredFrame(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.configure(bg="#f7f7f7")

        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor="center")

        self.bind("<Configure>", self.center_container)

        # Пример логотипов (если есть такие файлы)
        # Пути можно подкорректировать, чтобы они соответствовали вашим реальным asset-ам
        self.left_logo_path = "ui/assets/logo.png"
        self.right_logo_path = "ui/assets/logo.png"

        try:
            self.left_logo = ImageTk.PhotoImage(Image.open(self.left_logo_path).resize((80, 80), Image.Resampling.LANCZOS))
            self.right_logo = ImageTk.PhotoImage(Image.open(self.right_logo_path).resize((80, 80), Image.Resampling.LANCZOS))

            self.left_logo_label = tk.Label(self, image=self.left_logo, bg="#f7f7f7")
            self.left_logo_label.place(relx=1.0, x=-10, y=10, anchor="ne")

            self.right_logo_label = tk.Label(self, image=self.right_logo, bg="#f7f7f7")
            self.right_logo_label.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        except:
            pass  # если нет логотипов, игнорируем

    def center_container(self, event=None):
        self.container.place(relx=0.5, rely=0.5, anchor="center")

    def add_to_container(self, widget):
        widget.pack(pady=10)
