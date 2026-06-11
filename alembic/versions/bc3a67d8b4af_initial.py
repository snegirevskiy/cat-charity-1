"""Initial

Revision ID: bc3a67d8b4af
Revises:
Create Date: 2026-06-11 21:53:14.557433

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc3a67d8b4af'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'charityproject',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=False),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )
    op.create_table(
        'donation',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('comment', sa.Text(), nullable=True),
        sa.Column('full_amount', sa.Integer(), nullable=False),
        sa.Column('invested_amount', sa.Integer(), nullable=True),
        sa.Column('fully_invested', sa.Boolean(), nullable=True),
        sa.Column('create_date', sa.DateTime(), nullable=True),
        sa.Column('close_date', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('donation')
    op.drop_table('charityproject')