"""Add share_results field to User model

Revision ID: add_share_results_field
Revises: caafc89d9a5f
Create Date: 2024-01-01 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'add_share_results_field'
down_revision = 'caafc89d9a5f'
branch_labels = None
depends_on = None


def upgrade():
    # Add share_results column to user table
    op.add_column('user', sa.Column('share_results', sa.Boolean(), nullable=False, server_default='0'))


def downgrade():
    # Remove share_results column from user table
    op.drop_column('user', 'share_results') 