import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///aviation_ergonomics.db")

DEBUG = True
SECRET_KEY = "your_secret_key_for_sessions"
