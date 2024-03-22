"""add uybor id column

Revision ID: e810e5713f7d
Revises: 963f0b583965
Create Date: 2024-03-22 15:21:44.904892

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e810e5713f7d'
down_revision: Union[str, None] = '677318b7c9a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('buildings', sa.Column('uybor_id', sa.Integer, nullable=True))


def downgrade() -> None:
    op.drop_column('buildings', 'uybor_id')
