"""add images table

Revision ID: 87094c40461b
Revises: f367c4ed3ccf
Create Date: 2024-02-27 01:50:06.930916

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '87094c40461b'
down_revision: Union[str, None] = 'f367c4ed3ccf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "images", 
        sa.Column('id', sa.Integer, autoincrement=True, primary_key=True),
        sa.Column("filename", sa.String(200)),
        sa.Column("url", sa.String(500), nullable=True),
        sa.Column("building_id", sa.Integer, sa.ForeignKey("buildings.id"))
    )


def downgrade() -> None:
    op.drop_table("images")
