"""First revision

Revision ID: 340f6976b6ce
Revises: 
Create Date: 2023-05-10 19:05:34.687780

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '340f6976b6ce'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', 
                    sa.Column('post_id', sa.Integer, primary_key=True, index=True, nullable=False), 
                    sa.Column('title', sa.String, nullable=False),
                    sa.Column('content', sa.String, nullable=False),
                    sa.Column('published', sa.Boolean(), server_default='false', nullable=True), 
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.sql.func.now(), nullable=False))


def downgrade() -> None:
    op.drop_table('posts')
