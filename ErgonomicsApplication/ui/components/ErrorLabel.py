# ui/components/ErrorLabel.py
import tkinter as tk

class ErrorLabel(tk.Label):
    def __init__(self, master, **kwargs):
        super().__init__(master, fg="red", bg="#f7f7f7", font=("Arial", 12), **kwargs)
