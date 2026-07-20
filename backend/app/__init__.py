import os
from urllib.parse import urlparse

import cloudinary
from flask import Flask

from app.config import CONFIG_BY_NAME
from app.extensions import cors, db, jwt, migrate


def create_app(config_name: str | None = None) -> Flask:
    config_name = config_name or os.environ.get("FLASK_ENV", "development")

    app = Flask(__name__)
    app.config.from_object(CONFIG_BY_NAME[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    if app.config["CLOUDINARY_URL"]:
        # cloudinary.config(cloudinary_url=...) no parsea nada (solo hace un
        # update() literal); el SDK solo auto-lee CLOUDINARY_URL de os.environ
        # una vez, al importarse el modulo. Para no depender de ese orden de
        # import, parseamos la URL nosotros y pasamos los valores explicitos.
        parsed = urlparse(app.config["CLOUDINARY_URL"])
        cloudinary.config(
            cloud_name=parsed.hostname,
            api_key=parsed.username,
            api_secret=parsed.password,
        )

    from app.models import (  # noqa: F401
        Cliente,
        Pedido,
        PedidoDetalle,
        Producto,
        Stock,
        StockMovimiento,
        Usuario,
        Venta,
        Visita,
    )

    from app.api.auth import auth_bp
    from app.api.clientes import clientes_bp
    from app.api.dashboard import dashboard_bp
    from app.api.pedidos import pedidos_bp
    from app.api.productos import productos_bp
    from app.api.stock import stock_bp
    from app.api.usuarios import usuarios_bp
    from app.api.ventas import ventas_bp
    from app.api.visitas import visitas_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(clientes_bp, url_prefix="/api/clientes")
    app.register_blueprint(productos_bp, url_prefix="/api/productos")
    app.register_blueprint(pedidos_bp, url_prefix="/api/pedidos")
    app.register_blueprint(ventas_bp, url_prefix="/api/ventas")
    app.register_blueprint(stock_bp, url_prefix="/api/stock")
    app.register_blueprint(visitas_bp, url_prefix="/api/visitas")
    app.register_blueprint(usuarios_bp, url_prefix="/api/usuarios")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")

    @app.get("/api/health")
    def health():
        return {"status": "ok"}

    return app
