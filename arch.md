```
aviation_ergonomics/
│
├── app/                     # Основное приложение
│   ├── __init__.py          # Инициализация пакета
│   ├── models.py            # Определения моделей SQLAlchemy
│   ├── schemas.py           # Схемы Pydantic для валидации
│   ├── database.py          # Настройка подключения к базе данных
│   ├── services.py          # Бизнес-логика (взаимодействие с БД)
│   ├── routes.py            # Основные маршруты приложения
│   ├── pvt.py               # Логика теста PVT
│   ├── nasa_tlx.py          # Логика теста NASA-TLX
│   ├── utils.py             # Утилиты (хелперы, общие функции)
│   └── main.py              # Точка входа в приложение
│
├── migrations/              # Миграции базы данных
│
├── tests/                   # Тесты для приложения
│   ├── test_pvt.py          # Тесты для PVT
│   ├── test_nasa_tlx.py     # Тесты для NASA-TLX
│   └── test_routes.py       # Тесты API
│
├── config.py                # Конфигурация приложения
├── requirements.txt         # Зависимости проекта
└── README.md                # Документация проекта
```