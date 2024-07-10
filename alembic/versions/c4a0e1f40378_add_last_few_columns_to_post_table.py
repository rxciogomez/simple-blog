"""add last few columns to post table

Revision ID: c4a0e1f40378
Revises: b56c793f63bd
Create Date: 2024-07-10 08:45:39.132370

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c4a0e1f40378'
down_revision = 'b56c793f63bd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
                'published', sa.Boolean(), nullable=False, server_default='TRUE')
                )
    op.add_column('posts', sa.Column(
                'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()'))
                )
    pass


def downgrade():
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    pass
