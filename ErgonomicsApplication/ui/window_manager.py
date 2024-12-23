# ui/window_manager.py

class WindowManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(WindowManager, cls).__new__(cls)
        return cls._instance

    def __init__(self, root):
        self.root = root
        self.frames = {}
        self.current_user_id = None  # <-- здесь храним ID пользователя после логина

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def create_and_register(self, name, frame_class, *args, **kwargs):
        frame = frame_class(self.root, *args, **kwargs)
        frame.grid(row=0, column=0, sticky="nsew")
        self.frames[name] = frame

    def show_frame(self, name, **kwargs):
        frame = self.frames.get(name)
        if frame:
            if hasattr(frame, "update_data"):
                frame.update_data(**kwargs)
            frame.tkraise()
        else:
            raise ValueError(f"Frame '{name}' не найден!")
