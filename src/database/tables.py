import sqlalchemy as sa
from typing import List

metadata = sa.MetaData()

field = sa.Table(
    'field',
    metadata,
    sa.Column('type', sa.String, nullable=False),
    sa.Column('name', sa.String, nullable=False),
    sa.Column('cartodb_id', sa.BigInteger, primary_key=True),
    sa.Column('type_geometry', sa.String, nullable=False),
    sa.Column('coordinates', sa.String, nullable=False),
)
