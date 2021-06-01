from .base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Currency(Base):
    __tablename__ = "currency"
    currency_id = Column("currency_id", Integer, primary_key=True)
    currency_name = Column("currency_name", String)
    isocode = Column("isocode", String)
    currency_ = relationship("Apartment", backref='curr')

