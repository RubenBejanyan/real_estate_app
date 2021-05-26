from .db_flask_sql import db


class City(db.Model):
    __tablename__ = "city"
    city_id = db.Column("city_id", db.Integer, primary_key=True, autoincrement=True)
    name = db.Column("name", db.String)
    city_ = db.relationship("Apartment", backref='location')
