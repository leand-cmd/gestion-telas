"""Asigna codigo_cliente a clientes existentes sin uno

Revision ID: d4e5f6a7b8c9
Revises: c3d4e5f6a7b8
Create Date: 2026-07-15 11:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd4e5f6a7b8c9'
down_revision = 'c3d4e5f6a7b8'
branch_labels = None
depends_on = None


def upgrade():
    conn = op.get_bind()
    clientes = sa.table(
        "clientes",
        sa.column("id", sa.Integer),
        sa.column("codigo_cliente", sa.String),
    )

    max_num = 0
    for (valor,) in conn.execute(sa.select(clientes.c.codigo_cliente)):
        if valor and valor.isdigit():
            max_num = max(max_num, int(valor))

    sin_codigo = conn.execute(
        sa.select(clientes.c.id)
        .where(clientes.c.codigo_cliente.is_(None))
        .order_by(clientes.c.id)
    ).fetchall()

    siguiente = max_num + 1
    for (cliente_id,) in sin_codigo:
        conn.execute(
            clientes.update()
            .where(clientes.c.id == cliente_id)
            .values(codigo_cliente=str(siguiente))
        )
        siguiente += 1


def downgrade():
    pass
