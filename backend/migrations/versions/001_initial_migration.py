"""initial migration

Revision ID: 001
Revises: 
Create Date: 2024-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Создаем таблицу users
    op.create_table('users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('login', sa.String(length=64), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    
    # Создаем индекс для логина
    op.create_index(op.f('ix_users_login'), 'users', ['login'], unique=True)
    op.create_index('ix_users_login_unique', 'users', ['login'], unique=True)


def downgrade():
    # Удаляем таблицу users
    op.drop_index('ix_users_login_unique', table_name='users')
    op.drop_index(op.f('ix_users_login'), table_name='users')
    op.drop_table('users')
