"""add foreign key to posts table

Revision ID: ecef489838ce
Revises: c4da0a5601a9
Create Date: 2023-04-02 17:49:30.393285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecef489838ce'
down_revision = 'c4da0a5601a9'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',
                  sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users',
                          local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
