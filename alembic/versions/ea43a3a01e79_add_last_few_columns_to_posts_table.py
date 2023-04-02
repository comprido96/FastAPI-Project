"""add last few columns to posts table

Revision ID: ea43a3a01e79
Revises: ecef489838ce
Create Date: 2023-04-02 17:54:02.921347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea43a3a01e79'
down_revision = 'ecef489838ce'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('published', sa.Boolean(), nullable=False, server_default="TRUE"),)
    op.add_column('posts',
                  sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
