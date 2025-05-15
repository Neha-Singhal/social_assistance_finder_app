"""Add phone_number to user

Revision ID: 3626451dcb35
Revises: dcab7ec59fdd
Create Date: 2025-05-15 15:38:37.367560

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '3626451dcb35'
down_revision: Union[str, None] = 'dcab7ec59fdd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('user', sa.Column('phone_number', sa.String(length=20), nullable=True))

def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user', 'phone_number')