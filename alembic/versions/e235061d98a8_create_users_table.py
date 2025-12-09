"""Create users table

Revision ID: e235061d98a8
Revises: f80a80141351
Create Date: 2025-12-09 10:32:16.560610

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e235061d98a8'
down_revision: Union[str, Sequence[str], None] = 'f80a80141351'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("user_id", sa.Integer, primary_key=True),
        sa.Column("name", sa.VARCHAR(20)),
        sa.Column("email", sa.VARCHAR, unique=True),
        sa.Column("password", sa.VARCHAR)

    )


def downgrade() -> None:
    op.drop_table("users")
