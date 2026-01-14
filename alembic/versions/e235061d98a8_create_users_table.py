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
down_revision: Union[str, Sequence[str], None] = '021b68fadc14'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.VARCHAR(), nullable=False),
        sa.Column("email", sa.VARCHAR(), unique=True, nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.true(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default=sa.false(), nullable=False),
        sa.Column("hashed_password", sa.String(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), server_default=sa.false(), nullable=False),
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
    op.drop_table("users")
