"""create cart table

Revision ID: ad20180fb386
Revises: 054a0e1b4263
Create Date: 2026-01-19 13:32:43.570575

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad20180fb386'
down_revision: Union[str, Sequence[str], None] = '054a0e1b4263'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "cart",
        sa.Column("id", sa.Integer(), primary_key=True, index=True, nullable=False),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("product_id", sa.Integer(),sa.ForeignKey("products.id", ondelete="CASCADE"), nullable=False),
        sa.Column("quantity", sa.Integer(), nullable=False),
        sa.Column("price", sa.Float(), nullable=False),
        sa.Column("total_price", sa.Float(), nullable=False)
    )


def downgrade() -> None:
    op.drop_table("cart")
