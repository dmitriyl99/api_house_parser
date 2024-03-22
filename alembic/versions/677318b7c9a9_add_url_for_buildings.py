"""add url for buildings

Revision ID: 677318b7c9a9
Revises: 963f0b583965
Create Date: 2024-03-21 12:24:30.711350

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '677318b7c9a9'
down_revision: Union[str, None] = '963f0b583965'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('buildings', sa.Column('url', sa.String(200), nullable=True))


def downgrade() -> None:
    op.drop_column('buildings', 'url')
