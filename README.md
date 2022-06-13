# Task_Bewise


## Запуск:

- Склонировать репозиторий 
- Создать файл .env, который копия .env.example, прописать туда переменные окружения
- Cоздать и запустить образ docker image командой: docker-compose up --build 
- После старта всех контейнеров можно переходить на host:port
- Документация расположена по адресу http://host:port/docs 

## Описание:
Проект полностью развёртывается в докере

- post v1/user {"questions_num": integer}  -  полученные ответы сохраняются в базе данных
- Запрос post http://0.0.0.0:5000/v1/user body {"questions_num": 1} 
- Ответ    [{"id":121269,"answer":"category","question":"You must be cognizant of misspellings in a catagory like this, otherwise you might be embarrassed","date":"2014-02-14"}]

## Стек

- Python 3.10
- PostgreSQL
- SQLAlchemy
- Alembic
- FastAPI
- Uvicorn
- httpx или aiohttp
# AEROSPACE
