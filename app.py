from flask import render_template, request
from config import app
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy import desc
from db.real_estate_db import RealEstateDB

from constants import MIN_PRICE, MAX_PRICE, MIN_AREA, MAX_AREA, MIN_FLOOR, MAX_FLOOR
from db.models import Apartment
from db.models import City
from db.models import Currency


class Form(FlaskForm):
    city = SelectField('city', choices=[])
    building_type = SelectField('building_type', choices=[])
    renovation = SelectField('renovation', choices=[])
    new_building = SelectField('new_building', choices=[(1, "Yes"), (0, 'No')])
    rooms = SelectField('rooms', choices=[(i, str(i)) for i in range(1, 5)] + [(5, "5+")])
    restroom = SelectField('restroom', choices=[(i, str(i)) for i in range(1, 3)] + [(3, "3+")])
    currency = SelectField('currency', choices=[])


@app.cli.command('update_db')
def update():
    db = RealEstateDB()
    db.update_db()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts', methods=("GET", "POST"), defaults={"page": 1})
@app.route('/posts/<int:page>', methods=("GET", "POST"))
def all_posts(page: int):
    form = Form()
    form.city.choices = [(city.city_id, city.name) for city in City.query.all()]
    form.building_type.choices = list({ap.building_type for ap in Apartment.query.all()})
    form.renovation.choices = list({ap.renovation for ap in Apartment.query.all()})
    form.currency.choices = [(currency.currency_id, currency.currency_name) for currency in Currency.query.all()]

    _all_posts = Apartment.query.order_by(desc(Apartment.creation_date)).paginate(per_page=20, page=page)
    all_currency = [Currency.query.filter(Currency.currency_id == post.currency_id).first() for post in
                    _all_posts.items]

    return render_template("new_posts.html", all_posts=_all_posts, all_currency=all_currency, form=form)


@app.route('/posts_filtered', defaults={"page": 1})
@app.route('/posts_filtered/<int:page>')
def filtered_posts(page: int):
    form = Form()

    city_list = [(city.city_id, city.name) for city in City.query.all()]
    building_type_list = list({ap.building_type for ap in Apartment.query.all()})
    renovation_type_list = list({ap.renovation for ap in Apartment.query.all()})
    currency_list = [(currency.currency_id, currency.currency_name) for currency in Currency.query.all()]

    price1 = request.args.get('price1')
    price2 = request.args.get('price2')
    area1 = request.args.get('area1')
    area2 = request.args.get('area2')
    floor1 = request.args.get('floor1')
    floor2 = request.args.get('floor2')
    renovation = request.args.get('renovation')
    building_type = request.args.get('building_type')
    currency = request.args.get('currency')
    rest = request.args.get('restroom')
    new_building = request.args.get('new_building')
    rooms = request.args.get('rooms')
    city_id = request.args.get('city')

    filtered = Apartment.query.filter(Apartment.city_id == city_id,
                                      Apartment.rooms == rooms if rooms != "5" else Apartment.rooms > 4,
                                      Apartment.restrooms == rest if rest != "3" else Apartment.restrooms > 2,

                                      (price1 if price1 != '' else MIN_PRICE) <= Apartment.price,  # Price Filtering
                                      Apartment.price <= (price2 if price2 != '' else MAX_PRICE),

                                      (area1 if area1 != '' else MIN_AREA) <= Apartment.area,  # Area filtering
                                      Apartment.area <= (area2 if area2 != '' else MAX_AREA),

                                      (floor1 if floor1 != '' else MIN_FLOOR) <= Apartment.floor,  # Floor filtering
                                      Apartment.floor <= (floor2 if floor2 != '' else MAX_FLOOR),

                                      Apartment.renovation == renovation,
                                      Apartment.new_building == new_building,
                                      Apartment.building_type == building_type,
                                      Apartment.currency_id == currency
                                      ).order_by(desc(Apartment.creation_date)).paginate(per_page=20, page=page)

    filtered_currency = [Currency.query.filter(Currency.currency_id == post.currency_id).first() for post in
                         filtered.items]

    first_city = city_list.pop(int(city_id) - 1)
    form.city.choices = [first_city] + city_list

    first_room = form.rooms.choices.pop(int(rooms) - 1)
    form.rooms.choices = [first_room] + form.rooms.choices

    first_restroom = form.restroom.choices.pop(int(rest) - 1)
    form.restroom.choices = [first_restroom] + form.restroom.choices

    building_type_list.remove(building_type)
    form.building_type.choices = [building_type] + building_type_list

    renovation_type_list.remove(renovation)
    form.renovation.choices = [renovation] + renovation_type_list

    fist_new_building = form.new_building.choices.pop(int(new_building) - 1)
    form.new_building.choices = [fist_new_building] + form.new_building.choices

    first_currency = currency_list.pop(int(currency) - 1)
    form.currency.choices = [first_currency] + currency_list
    
    return render_template("filtered_posts.html", filtred=filtered, filtred_currency=filtered_currency, form=form,
                           price1=price1,
                           price2=price2,
                           area1=area1,
                           area2=area2,
                           floor1=floor1,
                           floor2=floor2
                           )


@app.route('/item/<id>')
def post_information(id: int):
    one_post = Apartment.query.filter_by(id=id).first()
    currency = Currency.query.filter_by(currency_id=one_post.currency_id).first()
    city = City.query.filter_by(city_id=one_post.city_id).first()
    return render_template("more_info.html", one_post=one_post, currency=currency, city=city)


if __name__ == "__main__":
    app.run(debug=True)
