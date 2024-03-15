"""create buildings table

Revision ID: 016e433bab84
Revises: b1302c6e16b3
Create Date: 2024-02-21 16:04:01.078028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '016e433bab84'
down_revision: Union[str, None] = 'b1302c6e16b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "buildings",
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column('territory', sa.String(100), nullable=True),
        sa.Column('area', sa.String(100), nullable=True),
        sa.Column('category_id', sa.Integer, sa.ForeignKey('categories.id')),
        sa.Column('sell_type', sa.String(20)),
        sa.Column('room_number', sa.Integer),
        sa.Column('land_area', sa.Float, nullable=True),
        sa.Column('building_area', sa.Float),
        sa.Column('price', sa.BigInteger),
        sa.Column('floor', sa.Integer),
        sa.Column('floor_number', sa.Integer),
        sa.Column('building_repair', sa.Text),
        sa.Column('type_of_ad', sa.String(100)),
        sa.Column('created_at', sa.DateTime, server_default=sa.sql.func.now()),
        sa.Column('source', sa.String(20)),
    )


def downgrade() -> None:
    op.drop_table('buildings')
