# server/models.py
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates

db = SQLAlchemy()

class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)

    # One-to-many relationship with RestaurantPizza
    pizzas = db.relationship(
        "RestaurantPizza",
        back_populates="restaurant",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Restaurant {self.id}: {self.name}>"


class Pizza(db.Model):
    __tablename__ = "pizzas"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    ingredients = db.Column(db.String, nullable=False)

    # One-to-many relationship with RestaurantPizza
    restaurants = db.relationship(
        "RestaurantPizza",
        back_populates="pizza",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Pizza {self.id}: {self.name}>"


class RestaurantPizza(db.Model):
    __tablename__ = "restaurant_pizzas"

    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)

    pizza_id = db.Column(db.Integer, db.ForeignKey("pizzas.id"))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"))

    # Relationships
    pizza = db.relationship("Pizza", back_populates="restaurants")
    restaurant = db.relationship("Restaurant", back_populates="pizzas")

    @validates("price")
    def validate_price(self, key, price):
        if price < 1 or price > 30:
            raise ValueError("Price must be between 1 and 30")
        return price

    def __repr__(self):
        return f"<RestaurantPizza {self.id}: Pizza {self.pizza_id} at Restaurant {self.restaurant_id} for {self.price}>"
