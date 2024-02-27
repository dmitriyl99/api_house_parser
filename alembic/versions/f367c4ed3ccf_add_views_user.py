"""add views user

Revision ID: f367c4ed3ccf
Revises: 016e433bab84
Create Date: 2024-02-27 01:34:09.629653

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f367c4ed3ccf'
down_revision: Union[str, None] = '016e433bab84'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("buildings", sa.Column("views", sa.Integer, default=0))
    op.add_column("buildings", sa.Column("user_name", sa.String(200), nullable=True))
    op.add_column("buildings", sa.Column("user_phone", sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column("buildings", "views")
    op.drop_column("buildings", "user_name")
    op.drop_column("buildings", "user_phone")
