# app/services/__init__.py
from .UserService import UserService
from .TestService import TestService

class Services:
    user = UserService()
    test = TestService()

    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = object.__new__(cls, *args, **kwargs)
        return cls._instance
