import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "dev-jwt-secret-key")

    _raw_database_url = os.environ.get("DATABASE_URL", "")
    if _raw_database_url:
        SQLALCHEMY_DATABASE_URI = _raw_database_url.replace(
            "postgres://", "postgresql+psycopg://", 1
        ).replace("postgresql://", "postgresql+psycopg://", 1)
    else:
        # Fallback local para poder levantar el servidor antes de tener la
        # DATABASE_URL de Railway. En produccion siempre debe setearse DATABASE_URL.
        SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "dev.db"
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    CORS_ORIGINS = [
        origin.strip()
        for origin in os.environ.get("CORS_ORIGINS", "http://localhost:5173").split(",")
        if origin.strip()
    ]

    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB

    GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")
    GOOGLE_CALENDAR_CLIENT_ID = os.environ.get("GOOGLE_CALENDAR_CLIENT_ID", "")
    GOOGLE_CALENDAR_CLIENT_SECRET = os.environ.get("GOOGLE_CALENDAR_CLIENT_SECRET", "")

    SMTP_HOST = os.environ.get("SMTP_HOST", "")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
    SMTP_USER = os.environ.get("SMTP_USER", "")
    SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
    SMTP_FROM = os.environ.get("SMTP_FROM", "")

    CLOUDINARY_URL = os.environ.get("CLOUDINARY_URL", "")

    EMAIL_COLABORADORES = [
        e.strip() for e in os.environ.get("EMAIL_COLABORADORES", "").split(",") if e.strip()
    ]


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    JWT_SECRET_KEY = "test-jwt-secret-key"


CONFIG_BY_NAME = {
    "development": Config,
    "production": Config,
    "testing": TestingConfig,
}
