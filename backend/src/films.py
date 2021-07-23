from flask import Blueprint, request, jsonify
from models import Film

bp = Blueprint("films", __name__, url_prefix="/films")


@bp.route("/")
def get_films():
    page_num = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    films = Film.query.paginate(
        per_page=per_page, page=page_num, error_out=False
    )

    items = [f.as_dict() for f in films.items]

    return jsonify(
        {"items": items, "total": films.total, "pages": films.pages}
    )
