from flask import render_template, request
from config import app
from flask_wtf import FlaskForm
from wtforms import SelectField
from sqlalchemy import desc

from constants import MIN_PRICE, MAX_PRICE
from db.models import Apartment
from db.models import City
from db.models import Currency


class Form(FlaskForm):
    city = SelectField('city', choices=[])
    rooms = SelectField('rooms', choices=[(i, str(i)) for i in range(1, 5)] + [(6, "5+")])


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

    if request.method == "POST":
        price1 = request.form.get("price1")
        price2 = request.form.get("price2")
        rooms = form.rooms.data
        filtred = Apartment.query.filter(Apartment.city_id == form.city.data,
                                         Apartment.rooms == rooms if rooms != "6" else Apartment.rooms >= 6,
                                         (price1 if price1 != '' else MIN_PRICE) <= Apartment.price,
                                         Apartment.price <= (price2 if price2 != '' else MAX_PRICE)
                                         ).order_by(desc(Apartment.creation_date)).paginate(per_page=20,
                                                                                            page=page)

        filtred_currency = [Currency.query.filter(Currency.currency_id == post.currency_id).first() for post in
                            filtred.items]

        return render_template("filtered_posts.html", filtred=filtred, filtred_currency=filtred_currency, form=form,
                               price1=price1,
                               price2=price2)

    _all_posts = Apartment.query.order_by(desc(Apartment.creation_date)).paginate(per_page=20, page=page)
    all_currency = [Currency.query.filter(Currency.currency_id == post.currency_id).first() for post in _all_posts.items]

    return render_template("new_posts.html", all_posts=_all_posts, all_currency=all_currency, form=form)


@app.route('/item/<id>')
def post_information(id: int):
    one_post = Apartment.query.filter_by(id=id).first()
    currency = Currency.query.filter_by(currency_id=one_post.currency_id).first()
    city = City.query.filter_by(city_id=one_post.city_id).first()
    return render_template("more_info.html", one_post=one_post, currency=currency, city=city)


if __name__ == "__main__":
    app.run(debug=True)
