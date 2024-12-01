class WindowManager:
    def __init__(self, root):
        self.root = root
        self.frames = {}

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_and_register(self, name, frame_class, *args, **kwargs):
        """Создает и регистрирует новый фрейм."""
        frame = frame_class(self.root, *args, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[name] = frame

    def show_frame(self, name, **kwargs):
        """Показывает фрейм по имени и передает аргументы."""
        frame = self.frames.get(name)
        if frame:
            if hasattr(frame, "update_data"):
                frame.update_data(**kwargs)
            frame.tkraise()
        else:
            raise ValueError(f"Frame '{name}' не найден!")
