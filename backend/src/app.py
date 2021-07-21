from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql://postgres:root@localhost:5432/dvdrental"

db = SQLAlchemy(app)


class Customer(db.Model):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    activebool = db.Column(db.Boolean)
    create_date = db.Column(db.Date)
    last_update = db.Column(db.Integer)
    address_id = db.Column(db.Integer, db.ForeignKey("address.id"))


class Address(db.Model):
    __tablename__ = "address"
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    address2 = db.Column(db.String())
    district = db.Column(db.String())
    postal_code = db.Column(db.String())
    phone = db.Column(db.String())
    last_update = db.Column(db.Integer)
    city_id = db.Column(db.Integer, db.ForeignKey("city.id"))


class City(db.Model):
    __tablename__ = "city"
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    last_update = db.Column(db.Integer)
    country_id = db.Column(db.Integer, db.ForeignKey("country.id"))


class Country(db.Model):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String())
    last_update = db.Column(db.Integer)


@app.route("/")
def hello_world():
    customer = Customer.query.first()
    address = Address.query.first()
    city = City.query.first()
    country = Country.query.first()
    print(customer, address, city, country)
    print(city.country_id)
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
