from flask import Blueprint, request, jsonify
from models import Customer

bp = Blueprint("customers", __name__)


@bp.route("/")
def get_customers():
    page_num = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 10, type=int)

    customers = Customer.query.paginate(
        per_page=per_page, page=page_num, error_out=False
    )

    items = [f.as_dict() for f in customers.items]

    return jsonify(
        {"items": items, "total": customers.total, "pages": customers.pages}
    )
