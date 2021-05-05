from sqlalchemy.orm import sessionmaker
from db.models import Base
from sqlalchemy import create_engine
from constants import DB_NAME
import os

engine = create_engine(f'sqlite:///{os.path.join("db", DB_NAME)}.db', echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
