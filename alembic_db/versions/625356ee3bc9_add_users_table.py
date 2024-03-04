"""add users table

Revision ID: 625356ee3bc9
Revises: 136b7aca1c2a
Create Date: 2024-03-03 02:43:28.041254

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '625356ee3bc9'
down_revision: Union[str, None] = '136b7aca1c2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
        op.create_table('users', 
                        sa.Column('id', sa.Integer(), nullable=False),
                        sa.Column('email', sa.String(), nullable=False),
                        sa.Column('password', sa.String(), nullable=False),
                        sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                  server_default=sa.text('now()'), nullable=False),
                        sa.PrimaryKeyConstraint('id'),
                        sa.UniqueConstraint('email')
                        )
    


def downgrade() -> None:
    op.drop_table('users')
    
