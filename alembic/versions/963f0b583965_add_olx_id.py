"""add olx id

Revision ID: 963f0b583965
Revises: 87094c40461b
Create Date: 2024-03-15 18:21:24.370649

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '963f0b583965'
down_revision: Union[str, None] = '87094c40461b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("buildings", sa.Column("olx_id", sa.BigInteger, nullable=True))


def downgrade() -> None:
    op.drop_column("buildings", "olx_id")
