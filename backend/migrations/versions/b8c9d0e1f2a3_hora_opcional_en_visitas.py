"""Hora opcional en visitas

Revision ID: b8c9d0e1f2a3
Revises: f6a7b8c9d0e1
Create Date: 2026-07-17 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b8c9d0e1f2a3'
down_revision = 'a7b8c9d0e1f2'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('visitas', schema=None) as batch_op:
        batch_op.alter_column('hora', existing_type=sa.Time(), nullable=True)


def downgrade():
    with op.batch_alter_table('visitas', schema=None) as batch_op:
        batch_op.alter_column('hora', existing_type=sa.Time(), nullable=False)
