from flask import Flask, render_template

from db.models.apartment_table import Apartment
from db.session import session

app = Flask(__name__)


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/posts')
def all_posts():
    all_posts = session.query(Apartment).all()
    return render_template("all_posts.html", all_posts=all_posts)


if __name__ == "__main__":
    app.run(debug=True)
