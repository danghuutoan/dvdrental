from flask import Flask, jsonify
from flask import request
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:root@localhost:5432/dvdrental"
    db.init_app(app)

    from models import (
        Customer,
        Address,
        City,
        Country,
        Store,
        Staff,
        Inventory,
        Payment,
        Film,
    )

    @app.route("/films")
    def get_films():
        page_num = (
            int(request.args.get("page")) if request.args.get("page") else None
        )
        per_page = (
            int(request.args.get("per_page"))
            if request.args.get("per_page")
            else 10
        )

        films = Film.query.paginate(
            per_page=per_page, page=page_num, error_out=False
        )

        items = [f.as_dict() for f in films.items]

        return jsonify(
            {"items": items, "total": films.total, "pages": films.pages}
        )

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
