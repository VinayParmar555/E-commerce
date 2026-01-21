"""create shipping_addresses table

Revision ID: 57a47bc38338
Revises: ad20180fb386
Create Date: 2026-01-21 12:04:42.271405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57a47bc38338'
down_revision: Union[str, Sequence[str], None] = 'ad20180fb386'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "shipping_addresses",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("address_line1", sa.String, nullable=False),
        sa.Column("address_line2", sa.String, nullable=True),
        sa.Column("city", sa.String, nullable=False),
        sa.Column("postal_code", sa.Integer, nullable=False),
        sa.Column("state", sa.String, nullable=False),
        sa.Column("country", sa.String, nullable=False)
    )

def downgrade() -> None:
    op.drop_table("shipping_addresses")
