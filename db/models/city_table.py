from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "city"
    city_id = Column("city_id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    city_ = relationship("Apartment", backref='location')
