from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config[
        "SQLALCHEMY_DATABASE_URI"
    ] = "postgresql://postgres:root@localhost:5432/dvdrental"
    db.init_app(app)

    from models import Customer, Address, City, Country

    @app.route("/")
    def hello_world():
        customer = Customer.query.first()
        address = Address.query.first()
        city = City.query.first()
        country = Country.query.first()
        print(customer, address, city, country)
        print(city.country_id)
        return "<p>Hello, World!</p>"

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
