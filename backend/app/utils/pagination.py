from flask import request


def paginate(query, default_per_page: int = 20, max_per_page: int = 100):
    try:
        page = max(int(request.args.get("page", 1)), 1)
    except ValueError:
        page = 1
    try:
        per_page = int(request.args.get("per_page", default_per_page))
    except ValueError:
        per_page = default_per_page
    per_page = max(1, min(per_page, max_per_page))

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "items": pagination.items,
        "page": pagination.page,
        "per_page": pagination.per_page,
        "total": pagination.total,
        "pages": pagination.pages,
    }
