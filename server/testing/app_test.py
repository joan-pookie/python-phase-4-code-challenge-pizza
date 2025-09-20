import pytest
from faker import Faker
from app import app, db
from models import Restaurant, Pizza, RestaurantPizza


class TestApp:
    """Flask application tests"""

    def setup_method(self):
        """Run before each test"""
        self.app = app.test_client()
        with app.app_context():
            db.drop_all()
            db.create_all()

    def teardown_method(self):
        """Run after each test"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_restaurants(self):
        """retrieves restaurants with GET request to /restaurants"""
        with app.app_context():
            fake = Faker()
            r1 = Restaurant(name=fake.name(), address=fake.address())
            r2 = Restaurant(name=fake.name(), address=fake.address())
            db.session.add_all([r1, r2])
            db.session.commit()

            res = self.app.get("/restaurants")
            assert res.status_code == 200
            data = res.get_json()
            assert len(data) == 2
            assert "name" in data[0]

    def test_create_restaurant_pizza_valid(self):
        """creates a RestaurantPizza with valid price"""
        with app.app_context():
            pizza = Pizza(name="Margherita", ingredients="Cheese, Tomato")
            restaurant = Restaurant(name="Test Place", address="123 Street")
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            res = self.app.post(
                "/restaurant_pizzas",
                json={
                    "price": 10,
                    "pizza_id": pizza.id,
                    "restaurant_id": restaurant.id,
                },
            )
            assert res.status_code == 201
            data = res.get_json()
            assert data["price"] == 10
            assert data["pizza"]["name"] == "Margherita"

    def test_create_restaurant_pizza_invalid_price(self):
        """fails when RestaurantPizza price is out of range"""
        with app.app_context():
            pizza = Pizza(name="Pepperoni", ingredients="Pepperoni, Cheese")
            restaurant = Restaurant(name="Test Place", address="123 Street")
            db.session.add_all([pizza, restaurant])
            db.session.commit()

            res = self.app.post(
                "/restaurant_pizzas",
                json={
                    "price": 50,
                    "pizza_id": pizza.id,
                    "restaurant_id": restaurant.id,
                },
            )
            assert res.status_code == 400
            data = res.get_json()
            assert "errors" in data
