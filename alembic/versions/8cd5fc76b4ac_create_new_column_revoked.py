"""create new column revoked

Revision ID: 8cd5fc76b4ac
Revises: e21bef9cce55
Create Date: 2025-12-17 20:59:54.829288

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cd5fc76b4ac'
down_revision: Union[str, Sequence[str], None] = 'e21bef9cce55'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "refresh_tokens", 
        sa.Column(
            "revoked",
            sa.Boolean(),
            server_default=sa.false(),
            nullable=False
        )
    )

def downgrade() -> None:
    op.drop_column("refresh_tokens", "revoked")
