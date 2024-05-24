"""Add content column to post table

Revision ID: c9029f0b0d6b
Revises: 26cd0af75a2c
Create Date: 2024-05-23 23:17:44.918002

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c9029f0b0d6b'
down_revision: Union[str, None] = '26cd0af75a2c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
