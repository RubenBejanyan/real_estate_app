from config import app
from flask_sqlalchemy import SQLAlchemy
from constants import DB_NAME
import os

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join("db", DB_NAME)}.db'
db = SQLAlchemy(app)


