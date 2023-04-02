"""add content column to posts table

Revision ID: 4955082d7d82
Revises: ed3d5e5cfd94
Create Date: 2023-04-02 17:37:37.552020

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4955082d7d82'
down_revision = 'ed3d5e5cfd94'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
