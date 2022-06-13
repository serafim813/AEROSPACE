"""
Create database

Revision ID: 33235f55faab
Revises: 
Create Date: 2022-05-5 11:39:29.055650
"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '33235f55faab'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'field',
        sa.Column('type', sa.String, nullable=False),
        sa.Column('name', sa.String, nullable=False),
        sa.Column('cartodb_id', sa.BigInteger, primary_key=True),
        sa.Column('type_geometry', sa.String, nullable=False),
        sa.Column('coordinates', sa.String, nullable=False),
        sa.PrimaryKeyConstraint('cartodb_id')
    )


def downgrade():
    op.drop_table('field')
