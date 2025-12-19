"""Create refresh_tokens table

Revision ID: e21bef9cce55
Revises: e235061d98a8
Create Date: 2025-12-16 23:11:48.566754

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e21bef9cce55'
down_revision: Union[str, Sequence[str], None] = 'e235061d98a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE")),
        sa.Column("token", sa.String(), nullable=False),
        sa.Column(
            "created_at", 
            sa.DateTime(timezone=True), 
            server_default=sa.func.now(),
            nullable=False
        ),
        sa.Column(
            "updated_at", 
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            server_onupdate=sa.func.now(), 
            nullable=False
        )

    )


def downgrade() -> None:
    op.drop_table("refresh_tokens")
