"""create new tables

Revision ID: cc69b18aa506
Revises: 57a47bc38338
Create Date: 2026-01-22 17:27:35.177021

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cc69b18aa506'
down_revision: Union[str, Sequence[str], None] = 'e063e15e6210'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "payment",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id", ondelete="CASCADE"), nullable=False),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("amount", sa.Integer, nullable=False),
        sa.Column("status", sa.Enum("pending", "success", "failed", "cancelled", name="payment_status_enum"), server_default="pending"),
        sa.Column("payment_gateway", sa.Enum("mock", "razorpay", name="payment_gateway_enum"), server_default="mock"),
        sa.Column("is_paid", sa.Boolean, server_default=sa.false()),
        sa.Column("pg_order_id", sa.String, nullable=True),
        sa.Column("pg_payment_id", sa.String, nullable=True),
        sa.Column("pg_signature", sa.String, nullable=True),
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
    op.drop_table("payment")