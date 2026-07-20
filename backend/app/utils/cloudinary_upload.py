import cloudinary.uploader
from flask import current_app


class CloudinaryNotConfiguredError(Exception):
    pass


def upload_imagen(file, folder: str = "productos") -> str:
    if not current_app.config["CLOUDINARY_URL"]:
        raise CloudinaryNotConfiguredError(
            "La subida de imagenes no esta configurada (falta CLOUDINARY_URL)"
        )
    result = cloudinary.uploader.upload(file, folder=folder)
    return result["secure_url"]
