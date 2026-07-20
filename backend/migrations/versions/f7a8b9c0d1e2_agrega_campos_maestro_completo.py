"""Agrega campos faltantes del maestro real (proveedor, marca, coleccion,
tipo_diseno, linea_sugerida, fecha_creacion, notas) y quita cod_categoria /
unidad_medida (no existen en el maestro real, eran especulativos)

Revision ID: f7a8b9c0d1e2
Revises: e2f3a4b5c6d7
Create Date: 2026-07-21 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f7a8b9c0d1e2'
down_revision = 'e2f3a4b5c6d7'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('cod_categoria')
        batch_op.drop_column('unidad_medida')

        batch_op.add_column(sa.Column('proveedor', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('marca', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('coleccion', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('tipo_diseno', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('linea_sugerida', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('fecha_creacion', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('notas', sa.Text(), nullable=True))


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('notas')
        batch_op.drop_column('fecha_creacion')
        batch_op.drop_column('linea_sugerida')
        batch_op.drop_column('tipo_diseno')
        batch_op.drop_column('coleccion')
        batch_op.drop_column('marca')
        batch_op.drop_column('proveedor')

        batch_op.add_column(sa.Column('unidad_medida', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('cod_categoria', sa.String(length=10), nullable=True))
