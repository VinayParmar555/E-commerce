"""create shipping_status tables

Revision ID: a8b378fe0c4f
Revises: 533da426d1db
Create Date: 2026-01-22 18:32:37.928062

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a8b378fe0c4f'
down_revision: Union[str, Sequence[str], None] = '533da426d1db'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shipping_status",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.Enum("pending", "processing", "shipped", "delivered", "cancelled", name="shipping_status_enum"), server_default="pending"),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), server_onupdate=sa.func.now(), nullable=False)

    )


def downgrade() -> None:
    op.drop_table("shipping_status")
