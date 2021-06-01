from .db_flask_sql import db


class Apartment(db.Model):
    __tablename__ = "apartment"
    id = db.Column('id', db.Integer, primary_key=True)
    creation_date = db.Column('creation_date', db.DateTime)
    update_date = db.Column('update_date', db.DateTime)
    img = db.Column("img", db.String)
    address = db.Column("address", db.String)
    price = db.Column("price", db.Integer)
    building_type = db.Column("building_type", db.String)
    new_building = db.Column("new_building", db.Boolean)
    elevator = db.Column("elevator", db.Boolean)
    floor = db.Column("floor", db.Integer)
    max_floor = db.Column("max_floor", db.Integer)
    rooms = db.Column("rooms", db.Integer)
    restrooms = db.Column("restrooms", db.Integer)
    area = db.Column("area", db.Integer)
    ceiling_height = db.Column("ceiling_height", db.String)
    balcony = db.Column("balcony", db.String)
    renovation = db.Column("renovation", db.String)
    city_id = db.Column(db.Integer, db.ForeignKey("city.city_id"))
    currency_id = db.Column(db.Integer, db.ForeignKey("currency.currency_id"))
