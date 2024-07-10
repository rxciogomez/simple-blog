"""Add content column to post table

Revision ID: 8a708366bfb8
Revises: 739881793e81
Create Date: 2024-07-09 13:31:25.536335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a708366bfb8'
down_revision = '739881793e81'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    
    pass


def downgrade():
    op.drop_column('posts','content')
    pass
