from .db_flask_sql import db


class Currency(db.Model):
    __tablename__ = "currency"
    currency_id = db.Column("currency_id", db.Integer, primary_key=True)
    currency_name = db.Column("currency_name", db.String)
    isocode = db.Column("isocode", db.String)
    currency_ = db.relationship("Apartment", backref='curr')
