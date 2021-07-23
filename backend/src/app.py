from flask import Flask, jsonify
from flask import request
from flask_migrate import Migrate
from models import setup_db
from models import Film


def create_app():
    app = Flask(__name__)

    db = setup_db(app)
    Migrate(app, db)
    import films

    app.register_blueprint(films.bp)

    return app

