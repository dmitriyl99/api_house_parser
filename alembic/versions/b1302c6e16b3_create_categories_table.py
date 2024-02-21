"""create categories table

Revision ID: b1302c6e16b3
Revises: 
Create Date: 2024-02-21 16:02:10.323291

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b1302c6e16b3'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('id', sa.BigInteger, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('parent_id', sa.BigInteger, nullable=True)
    )


def downgrade() -> None:
    op.drop_table('categories')
