"""create product table

Revision ID: f80a80141351
Revises: f00064e4799c
Create Date: 2025-12-08 08:42:29.990070

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f80a80141351'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table(
    "product",
    "products"
)

def downgrade() -> None:
    op.rename_table(
    "products",
    "product"
)
