from db.models import db, Apartment, City, Currency
from db.utils import create_city_dict
from scraper import scraping
from constants import ISO_CODE_DICT


class RealEstateDB:
    def __init__(self):
        db.create_all()
        self.session = db.session

    def update_db(self):
        for data, currency, city in scraping():
            city = create_city_dict(city)
            if not self.session.query(City).filter(City.name == city['name']).one_or_none():
                self.add_city(city)
            if not self.session.query(Currency).filter(Currency.currency_name == currency).one_or_none():
                self.add_currency(currency)
            apartment_in_db = self.session.query(Apartment).filter(Apartment.id == data["id"]).one_or_none()
            if apartment_in_db and apartment_in_db.update_date != data['update_date']:
                self.session.delete(apartment_in_db)
                self.add_apartment(data, currency, city)
            elif not apartment_in_db:
                self.add_apartment(data, currency, city)
            self.session.commit()
        self.session.close()

    def add_apartment(self, data, currency, city):
        cur_id = (self.session.query(Currency).filter(Currency.currency_name == currency).one()).currency_id
        cit_id = (self.session.query(City).filter(City.name == city['name']).one()).city_id
        apartment = Apartment(**data, currency_id=cur_id, city_id=cit_id)
        self.session.add(apartment)
        print(f'>>> Apartment added! ID: {data["id"]}')

    def add_city(self, city):
        city_ = City(**city)
        self.session.add(city_)
        print(f'>>> City added! Name: {city["name"]}')

    def add_currency(self, currency):
        currency_ = Currency(currency_name=currency, isocode=ISO_CODE_DICT[currency] if currency else None)
        self.session.add(currency_)
        print(f'>>> Currency added! Name: {currency}')
