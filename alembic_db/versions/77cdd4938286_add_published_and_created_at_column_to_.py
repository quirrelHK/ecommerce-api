"""add published and created_at column to posts

Revision ID: 77cdd4938286
Revises: 996549f9ee45
Create Date: 2024-03-03 02:56:27.097931

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '77cdd4938286'
down_revision: Union[str, None] = '996549f9ee45'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, 
                            server_default='TRUE'))
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), 
                            server_default=sa.text('now()'), nullable=False)
                  )
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','created_at')
    
    pass
