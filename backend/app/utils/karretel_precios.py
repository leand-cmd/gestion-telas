"""Lista de precios Karretel (PDF de referencia), usada para completar los
precios de un producto durante la importacion del maestro cuando el Excel
no trae precio_rollo/precio_media_rollo/precio_corte."""

PRECIOS_KARRETEL = [
    {"nombre_tejido": "Boston", "precio_rollo": 13900, "precio_media_rollo": None, "precio_corte": 16680},
    {"nombre_tejido": "Crepe Foil", "precio_rollo": 13500, "precio_media_rollo": None, "precio_corte": 18900},
    {"nombre_tejido": "Foil Knitting Stripe", "precio_rollo": 16500, "precio_media_rollo": 19800, "precio_corte": 23100},
    {"nombre_tejido": "Foil Washed Print", "precio_rollo": 19900, "precio_media_rollo": 23880, "precio_corte": 27860},
    {"nombre_tejido": "Marrakesh Print", "precio_rollo": 39300, "precio_media_rollo": 47160, "precio_corte": 51090},
    {"nombre_tejido": "Rayon Challis", "precio_rollo": 11300, "precio_media_rollo": None, "precio_corte": 13560},
    {"nombre_tejido": "Cotton Rayon", "precio_rollo": 19500, "precio_media_rollo": None, "precio_corte": 23400},
    {"nombre_tejido": "Rayon Baby Twill", "precio_rollo": 15900, "precio_media_rollo": None, "precio_corte": 19080},
    {"nombre_tejido": "Viscose Slub", "precio_rollo": 12900, "precio_media_rollo": None, "precio_corte": 15480},
    {"nombre_tejido": "Organic Garden", "precio_rollo": 88000, "precio_media_rollo": 105600, "precio_corte": 123200},
    {"nombre_tejido": "Delicata Flower", "precio_rollo": 15900, "precio_media_rollo": 19080, "precio_corte": 22260},
    {"nombre_tejido": "Milano F50 Span", "precio_rollo": 20900, "precio_media_rollo": None, "precio_corte": 25080},
    {"nombre_tejido": "Techno 160 Uni", "precio_rollo": 8500, "precio_media_rollo": None, "precio_corte": 11900},
    {"nombre_tejido": "Dynamic Supreme", "precio_rollo": 78000, "precio_media_rollo": 109200, "precio_corte": None},
    {"nombre_tejido": "Malha Fit Air", "precio_rollo": 42000, "precio_media_rollo": 58800, "precio_corte": None},
]

_PRECIOS_POR_TEJIDO = {p["nombre_tejido"].strip().lower(): p for p in PRECIOS_KARRETEL}


def buscar_precio_karretel(nombre_tejido: str) -> dict | None:
    if not nombre_tejido:
        return None
    return _PRECIOS_POR_TEJIDO.get(nombre_tejido.strip().lower())
