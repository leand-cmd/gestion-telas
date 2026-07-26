"""Agrega tabla grupos, grupo_id en colecciones, sku y nombre en productos

Revision ID: f8a9b0c1d2e3
Revises: 24d9e6739384
Create Date: 2026-07-25 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'f8a9b0c1d2e3'
down_revision = '24d9e6739384'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'grupos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('cod_grupo', sa.String(length=10), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('cod_grupo'),
    )
    op.create_index('ix_grupos_cod_grupo', 'grupos', ['cod_grupo'], unique=True)

    with op.batch_alter_table('colecciones', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grupo_id', sa.Integer(), nullable=True))
        batch_op.create_index('ix_colecciones_grupo_id', ['grupo_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_colecciones_grupo_id', 'grupos', ['grupo_id'], ['id']
        )

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('sku', sa.String(length=30), nullable=True))
        batch_op.add_column(sa.Column('nombre', sa.String(length=200), nullable=True))
        batch_op.create_index('ix_productos_sku', ['sku'], unique=True)


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_index('ix_productos_sku')
        batch_op.drop_column('nombre')
        batch_op.drop_column('sku')

    with op.batch_alter_table('colecciones', schema=None) as batch_op:
        batch_op.drop_constraint('fk_colecciones_grupo_id', type_='foreignkey')
        batch_op.drop_index('ix_colecciones_grupo_id')
        batch_op.drop_column('grupo_id')

    op.drop_index('ix_grupos_cod_grupo', table_name='grupos')
    op.drop_table('grupos')
