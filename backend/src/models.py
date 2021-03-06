from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.dialects.postgresql import TSVECTOR
import decimal

db = SQLAlchemy()
database_path = "postgresql://postgres:root@localhost:5432/dvdrental"


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    return db


class ModelMixin:
    def as_dict(self):
        obj_as_dict = {}
        for c in self.__table__.columns:
            value = getattr(self, c.name)

            if isinstance(value, decimal.Decimal):
                value = float(value)

            obj_as_dict[c.name] = value

        return obj_as_dict


class Customer(db.Model, ModelMixin):
    __tablename__ = "customer"
    customer_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    email = db.Column(db.String())
    activebool = db.Column(db.Boolean)
    create_date = db.Column(db.Date)
    last_update = db.Column(db.DateTime)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))
    store_id = db.Column(db.Integer, db.ForeignKey("store.store_id"))
    active = db.Column(db.Integer)


class Address(db.Model, ModelMixin):
    __tablename__ = "address"
    address_id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String())
    address2 = db.Column(db.String())
    district = db.Column(db.String())
    postal_code = db.Column(db.String())
    phone = db.Column(db.String())
    last_update = db.Column(db.DateTime)
    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"))


class City(db.Model, ModelMixin):
    __tablename__ = "city"
    city_id = db.Column(db.Integer, primary_key=True)
    city = db.Column(db.String())
    last_update = db.Column(db.DateTime)
    country_id = db.Column(db.Integer, db.ForeignKey("country.country_id"))


class Country(db.Model, ModelMixin):
    __tablename__ = "country"
    country_id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String())
    last_update = db.Column(db.DateTime)


class Store(db.Model, ModelMixin):
    __tablename__ = "store"
    store_id = db.Column(db.Integer, primary_key=True)
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))
    last_update = db.Column(db.DateTime)
    manager_staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"))


class Staff(db.Model, ModelMixin):
    __tablename__ = "staff"
    staff_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    address_id = db.Column(db.Integer, db.ForeignKey("address.address_id"))
    email = db.Column(db.String())
    store_id = db.Column(db.Integer, db.ForeignKey("store.store_id"))
    active = db.Column(db.Integer)
    username = db.Column(db.String())
    password = db.Column(db.String())
    last_update = db.Column(db.DateTime)
    picture = db.Column(db.LargeBinary)


class Inventory(db.Model, ModelMixin):
    __tablename__ = "inventory"
    inventory_id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, db.ForeignKey("film.film_id"))
    store_id = db.Column(db.Integer, db.ForeignKey("store.store_id"))
    last_update = db.Column(db.DateTime)


class Rental(db.Model, ModelMixin):
    __tablename__ = "rental"
    rental_id = db.Column(db.Integer, primary_key=True)
    rental_date = db.Column(db.DateTime)
    inventory_id = db.Column(
        db.Integer, db.ForeignKey("inventory.inventory_id")
    )
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    return_date = db.Column(db.DateTime)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"))
    last_update = db.Column(db.DateTime)


class Payment(db.Model, ModelMixin):
    __tablename__ = "payment"
    payment_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("customer.customer_id"))
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.staff_id"))
    rental_id = db.Column(db.Integer, db.ForeignKey("rental.rental_id"))
    amount = db.Column(db.Numeric(5, 2))
    payment_date = db.Column(db.DateTime)


class Actor(db.Model, ModelMixin):
    __tablename__ = "actor"
    actor_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String())
    last_name = db.Column(db.String())
    last_update = db.Column(db.DateTime)


class FilmActor(db.Model, ModelMixin):
    __tablename__ = "film_actor"
    actor_id = db.Column(db.Integer, primary_key=True)
    film_id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)


class Language(db.Model, ModelMixin):
    __tablename__ = "language"
    language_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    last_update = db.Column(db.DateTime)


class Film(db.Model, ModelMixin):
    __tablename__ = "film"
    film_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String())
    description = db.Column(db.Text())
    release_year = db.Column(db.Integer)
    language_id = db.Column(db.Integer, db.ForeignKey("language.language_id"))
    rental_duration = db.Column(db.SmallInteger)
    rental_rate = db.Column(db.Numeric(4, 2))
    length = db.Column(db.SmallInteger)
    replacement_cost = db.Column(db.Numeric(4, 2))
    rating = db.Column(
        db.Enum("G", "PG", "PG-13", "R", "NC-17", name="mpaa_rating")
    )
    last_update = db.Column(db.DateTime)
    special_features = db.Column(db.ARRAY(db.Text))
    fulltext = db.Column(TSVECTOR)


class FilmCategory(db.Model, ModelMixin):
    __tablename__ = "film_category"
    film_id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer, primary_key=True)
    last_update = db.Column(db.DateTime)


class Category(db.Model, ModelMixin):
    __tablename__ = "category"
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String())
    last_update = db.Column(db.DateTime)
