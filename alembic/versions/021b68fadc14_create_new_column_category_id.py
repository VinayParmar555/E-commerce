"""create new column category_id

Revision ID: 021b68fadc14
Revises: f2a3135a19da
Create Date: 2026-01-07 23:57:03.294306

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '021b68fadc14'
down_revision: Union[str, Sequence[str], None] = 'f2a3135a19da'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "products",
        sa.Column(
            "category_id", 
            sa.Integer, 
            sa.ForeignKey("categories.id", onupdate="CASCADE", ondelete="CASCADE"), 
            nullable=True)
 )


def downgrade() -> None:
    op.drop_column("products", "category_id")
