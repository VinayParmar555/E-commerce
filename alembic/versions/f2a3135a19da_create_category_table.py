"""create category table

Revision ID: f2a3135a19da
Revises: 054a0e1b4263
Create Date: 2026-01-05 23:13:01.300502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f2a3135a19da'
down_revision: Union[str, Sequence[str], None] = '054a0e1b4263'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categories",
        sa.Column("id", sa.Integer(), primary_key=True, index=True),
        sa.Column("name", sa.VARCHAR(), nullable=False, unique=True)
    )


def downgrade() -> None:
    op.drop_table("categories")
