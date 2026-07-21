"""Quita columnas de productos que no estan en la lista de campos requeridos
(coleccion texto libre, nombre_tejido, url_imagen, fecha_creacion, notas).
El agrupamiento pasa a depender enteramente de coleccion_id (FK real).

Revision ID: c2d3e4f5a6b7
Revises: b1c2d3e4f5a6
Create Date: 2026-07-23 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'c2d3e4f5a6b7'
down_revision = 'b1c2d3e4f5a6'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_productos_nombre_tejido'))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('coleccion')
        batch_op.drop_column('nombre_tejido')
        batch_op.drop_column('url_imagen')
        batch_op.drop_column('fecha_creacion')
        batch_op.drop_column('notas')


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notas', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('fecha_creacion', sa.Date(), nullable=True))
        batch_op.add_column(sa.Column('url_imagen', sa.String(length=500), nullable=True))
        batch_op.add_column(sa.Column('nombre_tejido', sa.String(length=100), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('coleccion', sa.String(length=100), nullable=True))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column('nombre_tejido', server_default=None)

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_productos_nombre_tejido'), ['nombre_tejido'], unique=False)
