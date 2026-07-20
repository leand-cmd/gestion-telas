import io
import re
import unicodedata

import pandas as pd
from werkzeug.datastructures import FileStorage


class ImportError_(Exception):
    pass


def _normalize_column(col: str) -> str:
    """'Sub Categoría' -> 'sub_categoria', 'Cod Producto' -> 'cod_producto'.

    Los maestros reales llegan con headers en Title Case, con espacios y
    acentos (ej. planillas armadas a mano en Excel); esto los deja en el
    mismo snake_case que usamos como clave interna, sin exigirle al usuario
    que renombre columnas antes de subir el archivo."""
    col = str(col).strip().lower()
    col = "".join(c for c in unicodedata.normalize("NFKD", col) if not unicodedata.combining(c))
    col = re.sub(r"[^\w]+", "_", col).strip("_")
    return col


def read_tabular_file(file: FileStorage) -> list[dict]:
    filename = (file.filename or "").lower()
    raw = file.read()

    if filename.endswith(".csv"):
        df = pd.read_csv(io.BytesIO(raw), dtype=str, keep_default_na=False)
    elif filename.endswith(".xlsx") or filename.endswith(".xls"):
        df = pd.read_excel(io.BytesIO(raw), dtype=str)
        df = df.fillna("")
    else:
        raise ImportError_("Formato no soportado. Use .csv, .xlsx o .xls")

    df.columns = [_normalize_column(c) for c in df.columns]
    return df.to_dict(orient="records")


def build_import_report(total_rows: int, inserted: int, errors: list[dict]) -> dict:
    return {
        "total_filas": total_rows,
        "insertados": inserted,
        "errores": errors,
        "cantidad_errores": len(errors),
    }
