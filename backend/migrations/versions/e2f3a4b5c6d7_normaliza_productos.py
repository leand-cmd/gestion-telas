"""Normaliza indice de cod_producto y ancho de sub_categoria

Revision ID: e2f3a4b5c6d7
Revises: d1e2f3a4b5c6
Create Date: 2026-07-20 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'e2f3a4b5c6d7'
down_revision = 'd1e2f3a4b5c6'
branch_labels = None
depends_on = None


def upgrade():
    # El indice unico de cod_producto quedo con el nombre legado de la
    # columna original (cod_sku) desde el primer rename; se corrige en su
    # propio batch para no repetir el conflicto de Alembic al recolectar
    # indices junto con otras operaciones de columna (ver migraciones
    # c9d0e1f2a3b4 / d1e2f3a4b5c6).
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_productos_cod_sku'))
        batch_op.create_index(batch_op.f('ix_productos_cod_producto'), ['cod_producto'], unique=True)

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column(
            'sub_categoria', existing_type=sa.String(length=100), type_=sa.String(length=50)
        )


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column(
            'sub_categoria', existing_type=sa.String(length=50), type_=sa.String(length=100)
        )

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_productos_cod_producto'))
        batch_op.create_index(batch_op.f('ix_productos_cod_sku'), ['cod_producto'], unique=True)
