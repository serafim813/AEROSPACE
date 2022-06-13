from typing import List, Dict

from sqlalchemy import select, delete
from sqlalchemy.future import Engine
import sqlalchemy as sa

from src.database import create_database_url
engine = sa.create_engine(
        create_database_url(),
        future=True
)
from src.tools.jservice_helper import Jservice
from src.database import tables
from src.user.models import (
    StatsAddV1,
    StatsAddV0,
    StatsAddV2,
)
import jsonpickle


class UserService:
    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    async def push_answers(self, type) -> None:
        """Check answers and push in databases"""
        def get_all_id_fields() -> Dict:
            query = select(tables.field.c.cartodb_id)
            with self._engine.connect() as connection:
                ids = connection.execute(query).fetchall()
            return {t_id[0] for t_id in ids}
        all_id_fields = get_all_id_fields()

        github = Jservice(self._engine)
        if type.properties.cartodb_id not in all_id_fields:
            github.push_answer_in_database(type)

        return

    def delete_field_by_id(self, name: str) -> None:
        query = delete(tables.field).where(tables.field.c.name == name)
        with self._engine.connect() as connection:
            connection.execute(query)
            connection.commit()

    def get_all_fields(self) -> List[StatsAddV1]:
        query = select(tables.field)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        for user_data in users_data:
            thawed = jsonpickle.decode(user_data['coordinates'])
        query = select(tables.field)
        with self._engine.connect() as connection:
            users_data = connection.execute(query)
        return [
                    StatsAddV1(
                        type=user_data['type'],
                        properties=StatsAddV0(
                            name=user_data['name'],
                            cartodb_id=user_data['cartodb_id']),
                        geometry=StatsAddV2(
                            type=user_data['type_geometry'],
                            coordinates=thawed)
                    ) for user_data in users_data
               ]
    # def get_last_answer(self, type) -> List[StatsAddV12]:
        # """Get last answer in databases"""
        # query = select(tables.field)
        # with self._engine.connect() as connection:
        #     fields = connection.execute(query)
        # return [StatsAddV1(
        #             type=type.type,
        #             name=type.properties.name,
        #             cartodb_id=type.properties.cartodb_id,
        #             type_geometry=type.geometry.type,
        #             coordinates=type.geometry.coordinates,
        # ) for field in fields
        # ]
