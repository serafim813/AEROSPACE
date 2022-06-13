from fastapi import APIRouter, status, Depends, File, Path
from fastapi.responses import FileResponse
import json
from src.api.protocols import UserServiceProtocol
from typing import List
from sqlalchemy.future import Engine
from src.user.models import StatsAddV1, StatsAddV2
from src.tools.jservice_helper import Jservice
import jsonpickle
#from src.tools.jservice_helper2 import get_NDVI

router = APIRouter(
    tags=['Users']
)

@router.post(
    path='/v1/user',
    status_code=status.HTTP_201_CREATED,
    summary='Добавить поле',
    description='Добавляет поле в бд',
)
async def add_answer(
    type: StatsAddV1,
    user_service: UserServiceProtocol = Depends()
):
    id_answer = await user_service.push_answers(type)

    return id_answer

some_file_path = "./src/tools/saved_figure.png"

@router.get("/files/", response_class=FileResponse)
async def get_field_image_from_NDVI():
    # a = get_NDVI()
    # print(a)
    return some_file_path


@router.delete(
    path='/v1/users/{name}',
    summary='Удалить поле',
    description='Удаляет поле.'
)
def delete_user(
    name: str = Path(...),
    user_service: UserServiceProtocol = Depends()
):
    user_service.delete_field_by_id(name)

@router.get(
    path='/v1/users',
    #response_model=List[StatsAddV1],
    summary='Список пользователей',
    description='Возвращает список всех пользователей.'
)
def get_all_users(
    user_service: UserServiceProtocol = Depends()
):
    return user_service.get_all_fields()

