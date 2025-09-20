#!/usr/bin/env python3

from app import app
from models import db, Restaurant, Pizza, RestaurantPizza

with app.app_context():
    print("Deleting data...")
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()

    print("Creating restaurants...")
    shack = Restaurant(name="Karen's Pizza Shack", address="address1")
    bistro = Restaurant(name="Sanjay's Pizza", address="address2")
    palace = Restaurant(name="Kiki's Pizza", address="address3")

    print("Creating pizzas...")
    cheese = Pizza(name="Emma", ingredients="Dough, Tomato Sauce, Cheese")
    pepperoni = Pizza(
        name="Geri",
        ingredients="Dough, Tomato Sauce, Cheese, Pepperoni"
    )
    california = Pizza(
        name="Melanie",
        ingredients="Dough, Sauce, Ricotta, Red peppers, Mustard"
    )

    print("Creating RestaurantPizza...")
    pr1 = RestaurantPizza(price=1, restaurant_id=1, pizza_id=1)
    pr2 = RestaurantPizza(price=4, restaurant_id=2, pizza_id=2)
    pr3 = RestaurantPizza(price=5, restaurant_id=3, pizza_id=3)

    db.session.add_all([shack, bistro, palace])
    db.session.add_all([cheese, pepperoni, california])
    db.session.commit()

    # Add restaurant pizzas after committing restaurants/pizzas
    db.session.add_all([pr1, pr2, pr3])
    db.session.commit()

    print("Seeding done!")
