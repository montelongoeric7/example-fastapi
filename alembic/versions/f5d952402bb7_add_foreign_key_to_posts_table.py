"""Add foreign key to posts table

Revision ID: f5d952402bb7
Revises: c706f1e928ac
Create Date: 2024-05-23 23:26:50.818327

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f5d952402bb7'
down_revision: Union[str, None] = 'c706f1e928ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('user_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk',source_table="posts",referent_table="users",local_cols=["user_id"],remote_cols=["id"],ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name='posts')
    op.drop_column('posts', 'user_id')
    pass
