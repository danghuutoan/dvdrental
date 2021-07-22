from flask import Flask, jsonify

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

    @app.route("/")
    def get_films():
        films = Film.query.limit(50).all()

        res = [f.as_dict() for f in films]

        return jsonify(res)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
