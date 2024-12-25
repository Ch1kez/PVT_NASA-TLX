import tkinter as tk


class StyledButton(tk.Button):
    def __init__(self, master, **kwargs):
        default_kwargs = {
            "font": ("Arial", 14),
            "bg": "#0047ab",
            "fg": "white",
            "activebackground": "#0051c7",
            "activeforeground": "white"
        }
        default_kwargs.update(kwargs)
        super().__init__(master, **default_kwargs)
