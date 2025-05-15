"""Add gemini_response to supportrequest

Revision ID: dcab7ec59fdd
Revises: 
Create Date: 2025-05-14 14:23:03.398626

"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'dcab7ec59fdd'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('supportrequest', sa.Column('gemini_response', sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column('supportrequest', 'gemini_response')