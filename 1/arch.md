```
aviation_ergonomics/
│
├── app/                     # Основное приложение
│   ├── __init__.py          # Инициализация пакета
│   ├── models.py            # Определения моделей SQLAlchemy
│   ├── schemas.py           # Схемы Pydantic для валидации
│   ├── database.py          # Настройка подключения к базе данных
│   ├── services.py          # Бизнес-логика (взаимодействие с БД)
│   ├── pvt.py               # Логика теста PVT
│   ├── nasa_tlx.py          # Логика теста NASA-TLX
│   ├── utils.py             # Утилиты (хелперы, общие функции)
│   └── main.py              # Точка входа в приложение
│
├── ui/                      # Интерфейс
│   ├── __init__.py          # Инициализация пакета UI
│   ├── main_window.py       # Главное окно приложения
│   ├── pvt_window.py        # Интерфейс теста PVT
│   ├── nasa_tlx_window.py   # Интерфейс NASA-TLX
│   └── results_window.py    # Окно для отображения результатов
│
├── migrations/              # Миграции базы данных
│
├── tests/                   # Тесты для приложения
│
├── config.py                # Конфигурация приложения
├── requirements.txt         # Зависимости проекта
└── README.md                # Документация проекта
```