import tkinter as tk

class NASA_TLXWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("NASA-TLX")
        self.geometry("400x600")

        self.labels = [
            "Mental Demand",
            "Physical Demand",
            "Temporal Demand",
            "Performance",
            "Effort",
            "Frustration"
        ]

        self.entries = {}
        for label in self.labels:
            tk.Label(self, text=label, font=("Arial", 12)).pack(pady=5)
            entry = tk.Entry(self)
            entry.pack(pady=5)
            self.entries[label] = entry

        submit_button = tk.Button(self, text="Сохранить результаты", command=self.save_results)
        submit_button.pack(pady=20)

    def save_results(self):
        results = {label: int(entry.get()) for label, entry in self.entries.items()}
        print("Результаты NASA-TLX:", results)
        self.destroy()
