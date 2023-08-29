import random

from flask import Flask, jsonify, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'

##Connect to Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cafes.db'
db = SQLAlchemy()
db.init_app(app)

##Cafe TABLE Configuration
class Cafe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), unique=True, nullable=False)
    map_url = db.Column(db.String(500), nullable=False)
    img_url = db.Column(db.String(500), nullable=False)
    location = db.Column(db.String(250), nullable=False)
    seats = db.Column(db.String(250), nullable=False)
    has_toilet = db.Column(db.Boolean, nullable=False)
    has_wifi = db.Column(db.Boolean, nullable=False)
    has_sockets = db.Column(db.Boolean, nullable=False)
    can_take_calls = db.Column(db.Boolean, nullable=False)
    coffee_price = db.Column(db.String(250), nullable=True)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/random", methods=["GET"])
def randomcafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    random_cafe = random.choice(all_cafes)
    print(random_cafe.name)
    cafe = {
        "Name": random_cafe.name,
        "Map URL": random_cafe.map_url,
        "img_url": random_cafe.img_url,
        "location": random_cafe.location,
        "seats": random_cafe.seats,
        "has_toilet": random_cafe.has_toilet,
        "has_wifi": random_cafe.has_wifi,
        "has_sockets": random_cafe.has_sockets,
        "can_take_calls": random_cafe.can_take_calls,
        "coffee_price": random_cafe.coffee_price
    }
    name = random_cafe.name
    return jsonify(cafe)
    

@app.route("/all", methods=["GET"])
def allcafe():
    result = db.session.execute(db.select(Cafe))
    all_cafes = result.scalars().all()
    cafes = []
    for cafe in all_cafes:

        cafe = {
            "Name": cafe.name,
            "id": cafe.id,
            "Map URL": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price
        }
        cafes.append(cafe)
    return jsonify(cafes)


@app.route("/search/", methods=["GET"])
def searchcafes():
    query_location = request.args.get("loc")
    results = db.session.execute(db.select(Cafe).where(Cafe.location == query_location.title())).scalars().all()
    cafes = []
    for cafe in results:
        cafe = {
            "Name": cafe.name,
            "Map URL": cafe.map_url,
            "img_url": cafe.img_url,
            "location": cafe.location,
            "seats": cafe.seats,
            "has_toilet": cafe.has_toilet,
            "has_wifi": cafe.has_wifi,
            "has_sockets": cafe.has_sockets,
            "can_take_calls": cafe.can_take_calls,
            "coffee_price": cafe.coffee_price
        }
        cafes.append(cafe)
    if cafes == []:
        return jsonify(Not_Found="Sorry no cafes exist in that location" )
    return jsonify(cafes)

@app.route("/new/", methods=["POST"])
def newcafes():
    cafe_name = request.form.get("name")
    print(request.form.get("name"))
    cafe = {
        "Name": request.form.get("name"),
        "Map URL": request.form.get("map_url"),
        "img_url": request.form.get("img_url"),
        "location": request.form.get("location").title(),
        "seats": bool(request.form.get("seats")),
        "has_toilet": bool(request.form.get("has_toilet")),
        "has_wifi": bool(request.form.get("has_wifi")),
        "has_sockets": bool(request.form.get("has_sockets")),
        "can_take_calls": bool(request.form.get("can_take_calls")),
        "coffee_price": request.form.get("coffee_price")
    }
    new_cafe = Cafe(
        name=cafe["Name"],
        map_url=cafe["Map URL"],
        img_url=cafe["img_url"],
        location=cafe["location"],
        seats=cafe["seats"],
        has_toilet=cafe["has_toilet"],
        has_wifi=cafe["has_wifi"],
        has_sockets=cafe["has_sockets"],
        can_take_calls=cafe["can_take_calls"],
        coffee_price=cafe["coffee_price"]
    )

    db.session.add(new_cafe)
    db.session.commit()
    Sucess = {
        "response":{
            "success": "A new film has been added"
        }
    }
    return jsonify(Sucess)


@app.route("/update-price/<cafe_id>", methods=["PATCH"])
def update_price(cafe_id):
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()
    if result == None:
        error = {
            "error": "there was an error"
        }
        return jsonify(error)
    else:
        new_price = request.form.get("price")
        result.coffee_price = new_price
        db.session.commit()
        success = {
            "success": "The coffee price has been updated"
        }
        return jsonify(success)


@app.route("/delete/<cafe_id>", methods=["DELETE"])
def delete(cafe_id):
    api_key = request.form.get("api-key")
    result = db.session.execute(db.select(Cafe).where(Cafe.id == cafe_id)).scalar()

    if api_key != "thisismyapikey":
        wrongkey = {
            "error": "Authenitation key invalid"
        }
        return jsonify(wrongkey)
    elif result == None:
        error = {
            "error": "there was an error"
        }
        return jsonify(error)
    else:
        db.session.delete(result)
        db.session.commit()
        success = {
            "success": "cafe has been removed"
        }
        return jsonify(success)
## HTTP GET - Read Record

## HTTP POST - Create Record

## HTTP PUT/PATCH - Update Record

## HTTP DELETE - Delete Record


if __name__ == '__main__':
    app.run(debug=True)
