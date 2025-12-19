"""create new column name expires_at for refresh_tokens table

Revision ID: 054a0e1b4263
Revises: 8cd5fc76b4ac
Create Date: 2025-12-19 18:32:53.185656

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '054a0e1b4263'
down_revision: Union[str, Sequence[str], None] = '8cd5fc76b4ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "refresh_tokens",
        sa.Column(
            "expires_at",
            sa.DateTime(timezone=True),
            nullable=False
        )
    )


def downgrade() -> None:
    op.drop_column("refresh_tokens", "expires_at")
