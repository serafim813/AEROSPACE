from typing import List

import aiohttp
from sqlalchemy import insert
from sqlalchemy.future import Engine

from src.user.models import StatsAddV1
from src.database import tables
import jsonpickle


class Jservice:
    """Class for parsing"""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def push_answer_in_database(self, type: StatsAddV1) -> None:
        frozen = jsonpickle.encode(type.geometry.coordinates)
        query = insert(tables.field).values(
            type=type.type,
            name=type.properties.name,
            cartodb_id=type.properties.cartodb_id,
            type_geometry=type.geometry.type,
            coordinates=frozen,
        )
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    # @staticmethod
    # async def get_answer_from_jservice(count) -> List[StatsAddV12]:
    #     """Get the right amount answers from jservice"""
    #     async with aiohttp.ClientSession() as session:
    #         async with session.get(URLGIT.format(count=count)) as r:
    #             return [
    #                 StatsAddV12(
    #                     id=res.pop('id'),
    #                     answer=res.pop('answer'),
    #                     question=res.pop('question'),
    #                     date=res.pop('created_at'),
    #                     **res,
    #                 ) for res in await r.json()
    #             ]