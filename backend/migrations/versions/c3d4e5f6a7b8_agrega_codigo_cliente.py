"""Agrega codigo_cliente a clientes

Revision ID: c3d4e5f6a7b8
Revises: b2c3d4e5f6a7
Create Date: 2026-07-15 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c3d4e5f6a7b8'
down_revision = 'b2c3d4e5f6a7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('codigo_cliente', sa.String(length=50), nullable=True))
        batch_op.create_index(
            batch_op.f('ix_clientes_codigo_cliente'), ['codigo_cliente'], unique=True
        )


def downgrade():
    with op.batch_alter_table('clientes', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_clientes_codigo_cliente'))
        batch_op.drop_column('codigo_cliente')
