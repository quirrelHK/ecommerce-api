"""add content column to posts table

Revision ID: 136b7aca1c2a
Revises: a8117f64fcff
Create Date: 2024-03-03 02:39:41.185364

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '136b7aca1c2a'
down_revision: Union[str, None] = 'a8117f64fcff'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
