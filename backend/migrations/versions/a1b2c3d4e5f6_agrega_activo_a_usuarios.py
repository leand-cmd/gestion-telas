"""Agrega columna activo a usuarios

Revision ID: a1b2c3d4e5f6
Revises: 82e41a2fb8a2
Create Date: 2026-07-13 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a1b2c3d4e5f6'
down_revision = '82e41a2fb8a2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('activo', sa.Boolean(), nullable=False, server_default=sa.true())
        )


def downgrade():
    with op.batch_alter_table('usuarios', schema=None) as batch_op:
        batch_op.drop_column('activo')
