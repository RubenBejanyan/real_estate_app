from .base import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime


class Apartment(Base):
    __tablename__ = "apartment"
    id = Column('id', Integer, primary_key=True)
    update_date = Column('update_date', DateTime)
    img = Column("img", String)
    address = Column("address", String)
    price = Column("price", Integer)
    building_type = Column("building_type", String)
    new_building = Column("new_building", Boolean)
    elevator = Column("elevator", Boolean)
    floor = Column("floor", Integer)
    max_floor = Column("max_floor", Integer)
    rooms = Column("rooms", Integer)
    restrooms = Column("restrooms", String)
    area = Column("area", Integer)
    ceiling_height = Column("ceiling_height", String)
    balcony = Column("balcony", String)
    renovation = Column("renovation", String)
    city_id = Column(Integer, ForeignKey("city.city_id"))
    currency_id = Column(Integer, ForeignKey("currency.currency_id"))
