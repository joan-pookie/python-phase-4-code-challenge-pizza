#!/usr/bin/env python3
import os
from flask import Flask, request, jsonify, make_response
from flask_migrate import Migrate
from flask_cors import CORS
from server.models import db, Restaurant, Pizza, RestaurantPizza

# ------------------ CONFIGURATION ------------------
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE = os.environ.get(
    "DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'app.db')}"
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

# Initialize extensions
db.init_app(app)
migrate = Migrate(app, db)
CORS(app)

# ------------------ ROUTES ------------------

@app.route("/")
def index():
    return "<h1>Code Challenge: Pizza Restaurants</h1>"

# ---------- RESTAURANTS ----------
@app.route("/restaurants", methods=["GET"])
def get_restaurants():
    restaurants = Restaurant.query.all()
    return make_response(
        [
            {"id": r.id, "name": r.name, "address": r.address}
            for r in restaurants
        ],
        200,
    )

@app.route("/restaurants/<int:id>", methods=["GET"])
def get_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    return make_response(
        {
            "id": restaurant.id,
            "name": restaurant.name,
            "address": restaurant.address,
            "restaurant_pizzas": [
                {
                    "id": rp.id,
                    "price": rp.price,
                    "pizza": {
                        "id": rp.pizza.id,
                        "name": rp.pizza.name,
                        "ingredients": rp.pizza.ingredients,
                    },
                }
                for rp in restaurant.restaurant_pizzas
            ],
        },
        200,
    )

@app.route("/restaurants/<int:id>", methods=["DELETE"])
def delete_restaurant(id):
    restaurant = Restaurant.query.get(id)
    if not restaurant:
        return make_response({"error": "Restaurant not found"}, 404)

    db.session.delete(restaurant)
    db.session.commit()
    return make_response({}, 204)

# ---------- PIZZAS ----------
@app.route("/pizzas", methods=["GET"])
def get_pizzas():
    pizzas = Pizza.query.all()
    return make_response(
        [{"id": p.id, "name": p.name, "ingredients": p.ingredients} for p in pizzas],
        200,
    )

# ---------- RESTAURANT PIZZAS ----------
@app.route("/restaurant_pizzas", methods=["POST"])
def create_restaurant_pizza():
    data = request.get_json()

    try:
        new_rp = RestaurantPizza(
            price=data["price"],
            pizza_id=data["pizza_id"],
            restaurant_id=data["restaurant_id"],
        )
        db.session.add(new_rp)
        db.session.commit()

        return make_response(
            {
                "id": new_rp.id,
                "price": new_rp.price,
                "pizza": {
                    "id": new_rp.pizza.id,
                    "name": new_rp.pizza.name,
                    "ingredients": new_rp.pizza.ingredients,
                },
            },
            201,
        )

    except ValueError as e:
        return make_response({"errors": [str(e)]}, 400)


# ------------------ RUN APP ------------------
if __name__ == "__main__":
    app.run(port=5555, debug=True)
