"""Reemplaza campos de productos por el maestro Karretel (rollo/media/corte)

Revision ID: d1e2f3a4b5c6
Revises: c9d0e1f2a3b4
Create Date: 2026-07-19 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'd1e2f3a4b5c6'
down_revision = 'c9d0e1f2a3b4'
branch_labels = None
depends_on = None


def upgrade():
    # 1) renombres y cambios de tipo/nullable sobre columnas existentes
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column('cod_producto', existing_type=sa.String(length=100), type_=sa.String(length=20))
        batch_op.alter_column('cod_color', existing_type=sa.String(length=50), type_=sa.String(length=20))
        batch_op.alter_column('subcategoria', new_column_name='sub_categoria')
        batch_op.alter_column('imagen_url', new_column_name='url_imagen')
        batch_op.alter_column('descripcion_completa', new_column_name='descripcion')
        batch_op.alter_column('estado', new_column_name='activo')
        batch_op.alter_column('stock_actual', new_column_name='stock_rollos', existing_type=sa.Integer(), nullable=True)
        batch_op.alter_column('categoria', existing_type=sa.String(length=50), nullable=False)

    # 2) eliminar columnas que ya no existen en el maestro Karretel
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('marca')
        batch_op.drop_column('linea')
        batch_op.drop_column('piezas')
        batch_op.drop_column('precio')
        batch_op.drop_column('stock_minimo')
        batch_op.drop_column('origen')
        batch_op.drop_column('codigo_base')
        batch_op.drop_column('color_categoria')
        batch_op.drop_column('diseno')
        batch_op.drop_column('medida')
        batch_op.drop_column('color')

    # 3) agregar columnas nuevas (sin indices todavia)
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cod_categoria', sa.String(length=10), nullable=True))
        batch_op.add_column(sa.Column('nombre_tejido', sa.String(length=100), nullable=False, server_default=''))
        batch_op.add_column(sa.Column('color_general', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('color_descripcion', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('composicion', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('ancho_cm', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('gramaje_gm2', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('precio_rollo', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('precio_media_rollo', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('precio_corte', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('unidad_medida', sa.String(length=50), nullable=True, server_default='metro'))

    # 4) limpiar server_default temporales usados solo para poblar la columna NOT NULL
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column('nombre_tejido', server_default=None)
        batch_op.alter_column('unidad_medida', server_default=None)

    # 5) indices nuevos, en su propio batch para evitar el conflicto de Alembic
    #    al recolectar indices de una tabla que acaba de renombrar/agregar columnas
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_productos_categoria'), ['categoria'], unique=False)
        batch_op.create_index(batch_op.f('ix_productos_activo'), ['activo'], unique=False)
        batch_op.create_index(batch_op.f('ix_productos_nombre_tejido'), ['nombre_tejido'], unique=False)


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_productos_nombre_tejido'))
        batch_op.drop_index(batch_op.f('ix_productos_activo'))
        batch_op.drop_index(batch_op.f('ix_productos_categoria'))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('unidad_medida')
        batch_op.drop_column('precio_corte')
        batch_op.drop_column('precio_media_rollo')
        batch_op.drop_column('precio_rollo')
        batch_op.drop_column('gramaje_gm2')
        batch_op.drop_column('ancho_cm')
        batch_op.drop_column('composicion')
        batch_op.drop_column('color_descripcion')
        batch_op.drop_column('color_general')
        batch_op.drop_column('nombre_tejido')
        batch_op.drop_column('cod_categoria')

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('color', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('medida', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('diseno', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('color_categoria', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('codigo_base', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('origen', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('stock_minimo', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('precio', sa.Numeric(precision=12, scale=2), nullable=True))
        batch_op.add_column(sa.Column('piezas', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('linea', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('marca', sa.String(length=255), nullable=True))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column('categoria', existing_type=sa.String(length=50), nullable=True)
        batch_op.alter_column('stock_rollos', new_column_name='stock_actual', existing_type=sa.Integer(), nullable=False)
        batch_op.alter_column('activo', new_column_name='estado')
        batch_op.alter_column('descripcion', new_column_name='descripcion_completa')
        batch_op.alter_column('url_imagen', new_column_name='imagen_url')
        batch_op.alter_column('sub_categoria', new_column_name='subcategoria')
        batch_op.alter_column('cod_color', existing_type=sa.String(length=20), type_=sa.String(length=50))
        batch_op.alter_column('cod_producto', existing_type=sa.String(length=20), type_=sa.String(length=100))
