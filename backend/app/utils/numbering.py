def generate_correlative(model, field_name: str, prefix: str, width: int = 5) -> str:
    field = getattr(model, field_name)
    max_num = 0
    for (value,) in model.query.with_entities(field).all():
        if value and value.startswith(prefix):
            try:
                max_num = max(max_num, int(value[len(prefix):]))
            except ValueError:
                continue
    return f"{prefix}{max_num + 1:0{width}d}"


def generate_next_numeric_code(model, field_name: str) -> str:
    """Siguiente numero libre entre los valores puramente numericos de field_name.

    Ignora codigos personalizados no numericos (ej. "ABC-001"), asi que
    conviven codigos autoasignados y codigos manuales sin colisionar.
    """
    field = getattr(model, field_name)
    max_num = 0
    for (value,) in model.query.with_entities(field).all():
        if value and value.isdigit():
            max_num = max(max_num, int(value))
    return str(max_num + 1)
