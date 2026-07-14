import io

import pandas as pd
from werkzeug.datastructures import FileStorage


class ImportError_(Exception):
    pass


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

    df.columns = [str(c).strip().lower() for c in df.columns]
    return df.to_dict(orient="records")


def build_import_report(total_rows: int, inserted: int, errors: list[dict]) -> dict:
    return {
        "total_filas": total_rows,
        "insertados": inserted,
        "errores": errors,
        "cantidad_errores": len(errors),
    }
