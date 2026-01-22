"""create new tables

Revision ID: e063e15e6210
Revises: cc69b18aa506
Create Date: 2026-01-22 18:04:27.929156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e063e15e6210'
down_revision: Union[str, Sequence[str], None] = '57a47bc38338'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "orders",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("shipping_address_id", sa.Integer, sa.ForeignKey("shipping_addresses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("total_price", sa.Float, nullable=False),
        sa.Column("status", sa.Enum("pending", "confirmed", "cancelled", name="order_status_enum"), server_default="pending"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False)
    )

def downgrade() -> None:
    op.drop_table("orders")
