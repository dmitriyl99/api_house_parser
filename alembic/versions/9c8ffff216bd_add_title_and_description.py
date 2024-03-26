"""add title and description

Revision ID: 9c8ffff216bd
Revises: e810e5713f7d
Create Date: 2024-03-26 17:09:10.656221

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9c8ffff216bd'
down_revision: Union[str, None] = 'e810e5713f7d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("buildings", sa.Column('title', sa.Text))
    op.add_column("buildings", sa.Column("description", sa.Text))


def downgrade() -> None:
    op.drop_column("buildings", "title")
    op.drop_column("buildings", "description")
