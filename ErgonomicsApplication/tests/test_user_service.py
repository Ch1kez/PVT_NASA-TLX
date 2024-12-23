# tests/test_user_service.py
from app.services import Services

def test_user_service_create():
    # Пример теста
    user_data = {"name": "Test User", "login": "testlogin", "password": "1234"}
    user_id = Services().user.create_user(user_data)
    assert user_id is not None
    user = Services().user.get_user_by_id(user_id=user_id)
    assert user is not "testlogin"