from flask import Flask, jsonify
from flask import request
from flask_migrate import Migrate
from models import setup_db
from models import Film


def create_app():
    app = Flask(__name__)

    db = setup_db(app)
    migrate = Migrate(app, db)

    @app.route("/films")
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

    return app

