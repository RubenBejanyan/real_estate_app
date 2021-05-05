from db.real_estate_db import RealEstateDB
from db.session import session


if __name__ == '__main__':
    data_base = RealEstateDB(session)
    data_base.update_db()
