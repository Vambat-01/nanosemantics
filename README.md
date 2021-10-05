# Web-приложение для хранения информации о сотрудниках компании

## Запуск Web-приложения используя [Docker](https://www.docker.com/)
1. Выставите переменные окружения. Сервер использует переменные `PG_USER` и `PG_PASSWORD` для авторизации в базе данных. При запуске через `docker-compose` (для локального тестирования), в качестве значений могут быть использованы любые строки. `docker-compose` выставит одинаковые значения и для базы и для сервера.
   1. `export PG_USER=<user val>`
   2. `export PG_PASSWORD=<password val>`

1. Cоздайте `Docker` образ приложения: `docker build -t web-app .`
1. Запустите web-приложение: `docker-compose up`

## Проверьте работоспособность web-приложения
1. Установите зависимости: `pip install -r requirements.txt`
1. Запустите системные тесты: `python -m unittest tests/system_tests.py`
1. Тесты должны успешно пройти

## Документация к сервису
- Перейдите по ссылке [openapi](http://localhost:8000/docs)