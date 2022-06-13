# AEROSPACE


## Запуск:

- Склонировать репозиторий 
- Создать файл .env, который копия .env.example, прописать туда переменные окружения
- Cоздать и запустить образ docker image командой: docker-compose up --build 
- После старта всех контейнеров можно переходить на host:port
- Документация расположена по адресу http://host:port/docs 

## Описание:
Проект полностью развёртывается в докере
Если используется Postman, то collection лежат в папке postman

## Стек

- Python 3.10
- PostgreSQL
- SQLAlchemy
- Alembic
- FastAPI
- Uvicorn
- httpx или aiohttp

