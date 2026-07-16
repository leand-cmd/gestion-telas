"""RUC opcional en clientes

Revision ID: a7b8c9d0e1f2
Revises: f6a7b8c9d0e1
Create Date: 2026-07-16 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a7b8c9d0e1f2'
down_revision = 'f6a7b8c9d0e1'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.alter_column('ruc', existing_type=sa.String(length=50), nullable=True)


def downgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.alter_column('ruc', existing_type=sa.String(length=50), nullable=False)
