"""Crea tabla colecciones

Revision ID: a9b0c1d2e3f4
Revises: f7a8b9c0d1e2
Create Date: 2026-07-22 09:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


revision = 'a9b0c1d2e3f4'
down_revision = 'f7a8b9c0d1e2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'colecciones',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('imagen_url', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    with op.batch_alter_table('colecciones', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_colecciones_nombre'), ['nombre'], unique=True)


def downgrade():
    with op.batch_alter_table('colecciones', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_colecciones_nombre'))

    op.drop_table('colecciones')
