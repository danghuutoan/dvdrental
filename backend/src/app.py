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


@app.route("/")
def hello_world():
    customer = Customer.query.first()
    print(customer)
    return "<p>Hello, World!</p>"


if __name__ == "__main__":
    app.run(host="0.0.0.0")
