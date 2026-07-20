"""Agrega coleccion_id (FK a colecciones) a productos

Revision ID: b1c2d3e4f5a6
Revises: a9b0c1d2e3f4
Create Date: 2026-07-22 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'b1c2d3e4f5a6'
down_revision = 'a9b0c1d2e3f4'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.add_column(sa.Column('coleccion_id', sa.Integer(), nullable=True))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_productos_coleccion_id'), ['coleccion_id'], unique=False)
        batch_op.create_foreign_key(
            'fk_productos_coleccion_id_colecciones', 'colecciones', ['coleccion_id'], ['id']
        )


def downgrade():
    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_constraint('fk_productos_coleccion_id_colecciones', type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_productos_coleccion_id'))

    with op.batch_alter_table('productos', schema=None) as batch_op:
        batch_op.drop_column('coleccion_id')
