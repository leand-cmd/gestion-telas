"""Capitaliza los valores de estado en pedidos existentes

Revision ID: f6a7b8c9d0e1
Revises: e5f6a7b8c9d0
Create Date: 2026-07-15 13:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f6a7b8c9d0e1'
down_revision = 'e5f6a7b8c9d0'
branch_labels = None
depends_on = None

MAPEO = {
    "borrador": "Pendiente",
    "confirmado": "Confirmado",
    "entregado": "Entregado",
    "facturado": "Facturado",
    "cancelado": "Cancelado",
}


def upgrade():
    conn = op.get_bind()
    pedidos = sa.table("pedidos", sa.column("estado", sa.String))

    for viejo, nuevo in MAPEO.items():
        conn.execute(pedidos.update().where(pedidos.c.estado == viejo).values(estado=nuevo))


def downgrade():
    conn = op.get_bind()
    pedidos = sa.table("pedidos", sa.column("estado", sa.String))

    for viejo, nuevo in MAPEO.items():
        conn.execute(pedidos.update().where(pedidos.c.estado == nuevo).values(estado=viejo))
