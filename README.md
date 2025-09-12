# Hital API – Сервис вопросов и ответов

API‑сервис для управления вопросами и ответами, построенный на [FastAPI](https://fastapi.tiangolo.com/) и PostgreSQL. Поддерживает миграции через Alembic, логирование и контейнеризацию через Docker.

## 🚀 Возможности

* Управление вопросами и ответами через REST API
* Автоматическая документация Swagger и ReDoc
* Миграции базы данных через Alembic
* Подробное логирование (консоль + файл)
* Лёгкий запуск через Docker и Docker Compose

## 🛠️ Стек технологий

* **Python 3.10+**
* **FastAPI** — backend-фреймворк
* **SQLAlchemy** — ORM для работы с базой данных
* **Alembic** — миграции
* **PostgreSQL** — основная база данных
* **pytest** — тестирование
* **Docker & Docker Compose** — контейнеризация и оркестрация

## 🔧 Окружения

В проекте используются два файла окружения:

* `.env` — для локального запуска и тестов (pytest)
* `.env-non-dev` — для запуска в Docker (docker-compose)

### Пример `.env`

```
MODE=DEV

DB_HOST=localhost
DB_PORT=5432
DB_USER=your_username
DB_PASS=your_password
DB_NAME=your_db_name

TEST_DB_HOST=localhost
TEST_DB_PORT=5432
TEST_DB_USER=your_username
TEST_DB_PASS=your_password
TEST_DB_NAME=your_db_name

LOG_LEVEL=INFO
```

### Пример `.env-non-dev`

```
MODE=PROD

DB_HOST=db
DB_PORT=5432
DB_USER=your_username
DB_PASS=your_password
DB_NAME=your_db_name

POSTGRES_DB=your_db_name
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password

LOG_LEVEL=INFO
```

> ⚠️ Для запуска в Docker **обязательно используйте `.env-non-dev`**, так как в нём указаны правильные хосты и настройки для контейнеров.

## ⚙️ Установка и запуск

### 1. Клонирование репозитория

```bash
git clone https://github.com/damonjiuc/Hital_API.git
cd Hital_API
```

### 2. Настройка окружения

Скопируйте пример `.env-non-dev` и настройте свои данные:

```bash
cp env-non-dev.example .env-non-dev
```

### 3. Запуск через Docker Compose

```bash
docker compose up --build
```

После успешного запуска:

* API: [http://localhost:8000](http://localhost:8000)
* Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
* ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### 4. Миграции базы данных

Миграции выполняются внутри контейнера

## 📖 API Endpoints

### Вопросы

* `GET /questions/` — список всех вопросов
* `POST /questions/` — создать новый вопрос
* `GET /questions/{id}` — получить вопрос и все ответы на него
* `DELETE /questions/{id}` — удалить вопрос (вместе с ответами)

### Ответы

* `POST /questions/{id}/answers/` — добавить ответ к вопросу
* `GET /answers/{id}` — получить конкретный ответ
* `DELETE /answers/{id}` — удалить ответ

## 🧪 Тестирование

Тесты запускаются на **локальной версии приложения** и используют настройки из `.env`.

```bash
pytest
```


## 📂 Структура проекта

```
Hital_api/
├── app/
│   ├── main.py           # Точка входа приложения
│   ├── config.py         # Настройки проекта
│   ├── schemas.py        # Pydantic-схемы
│   ├── tests/            # Тесты (Фикстуры, данные, тесты)
│   ├── services/         # Сервисы (Работа с БД, логирование)
│   ├── routers/          # Маршруты (questions, answers)
│   └── database/         # Подключение к БД, модели и миграции
├── alembic.ini           # Настройки Alembic
├── docker-compose.yml    # Конфигурация Docker Compose
├── Dockerfile            # Docker-образ приложения
├── requirements.txt      # Python-зависимости
└── README.md
```

## 📝 Логирование

Приложение записывает логи в консоль

Настройка уровня логирования через `.env` или `.env-non-dev`:

```
LOG_LEVEL=INFO
```
