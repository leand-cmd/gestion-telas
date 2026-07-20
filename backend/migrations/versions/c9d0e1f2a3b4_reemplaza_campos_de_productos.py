"""Reemplaza campos de productos por el nuevo catalogo

Revision ID: c9d0e1f2a3b4
Revises: b8c9d0e1f2a3
Create Date: 2026-07-18 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9d0e1f2a3b4'
down_revision = 'b8c9d0e1f2a3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        # El indice unico de cod_sku se conserva automaticamente al renombrar
        # la columna (Alembic actualiza los indices existentes en batch mode).
        batch_op.alter_column('cod_sku', new_column_name='cod_producto')
        batch_op.alter_column('descripcion', new_column_name='descripcion_completa')

        batch_op.drop_column('nro_producto')
        batch_op.drop_column('clase')
        batch_op.drop_column('metros')
        batch_op.drop_column('kilogramos')
        batch_op.drop_column('costo')

        batch_op.add_column(sa.Column('linea', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('subcategoria', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('cod_color', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('color_categoria', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('codigo_base', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('diseno', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('medida', sa.String(length=50), nullable=True))

        batch_op.alter_column('origen', existing_type=sa.String(length=50), type_=sa.String(length=100))


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.alter_column('origen', existing_type=sa.String(length=100), type_=sa.String(length=50))

        batch_op.drop_column('medida')
        batch_op.drop_column('diseno')
        batch_op.drop_column('codigo_base')
        batch_op.drop_column('color_categoria')
        batch_op.drop_column('cod_color')
        batch_op.drop_column('subcategoria')
        batch_op.drop_column('linea')

        batch_op.add_column(sa.Column('costo', sa.Numeric(precision=12, scale=2), nullable=True))
        batch_op.add_column(sa.Column('kilogramos', sa.Numeric(precision=10, scale=3), nullable=True))
        batch_op.add_column(sa.Column('metros', sa.Numeric(precision=10, scale=3), nullable=True))
        batch_op.add_column(sa.Column('clase', sa.String(length=50), nullable=True))
        batch_op.add_column(sa.Column('nro_producto', sa.Integer(), nullable=True))

        batch_op.alter_column('descripcion_completa', new_column_name='descripcion')
        batch_op.alter_column('cod_producto', new_column_name='cod_sku')
