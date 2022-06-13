from datetime import date, datetime

from pydantic import BaseModel, validator
from typing import List


class StatsAddV2(BaseModel):
    type: str
    coordinates: List[List[List[float]]]


class StatsAddV0(BaseModel):
    name: str
    cartodb_id: int


class StatsAddV1(BaseModel):
    type: str
    properties: StatsAddV0
    geometry: StatsAddV2
