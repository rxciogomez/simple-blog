"""create post table

Revision ID: 739881793e81
Revises: 
Create Date: 2024-07-09 12:15:46.622970

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '739881793e81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    
    pass


def downgrade():
    op.drop_table('posts')
    pass
