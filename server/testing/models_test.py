import pytest
from faker import Faker
from server.app import app
from server.models import db, Restaurant, Pizza, RestaurantPizza


@pytest.fixture(scope="function", autouse=True)
def app_context():
    """Create a fresh database for each test."""
    with app.app_context():
        db.create_all()
        yield
        db.session.remove()
        db.drop_all()


class TestRestaurantPizza:
    """Tests for RestaurantPizza model."""

    def test_price_between_1_and_30(self):
        """Allows prices at the boundaries 1 and 30."""

        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address="Main St")
        db.session.add(pizza)
        db.session.add(restaurant)
        db.session.commit()

        restaurant_pizza_1 = RestaurantPizza(
            restaurant_id=restaurant.id, pizza_id=pizza.id, price=1
        )
        restaurant_pizza_2 = RestaurantPizza(
            restaurant_id=restaurant.id, pizza_id=pizza.id, price=30
        )
        db.session.add_all([restaurant_pizza_1, restaurant_pizza_2])
        db.session.commit()

    def test_price_too_low(self):
        """Fails when price is below 1."""

        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address="Main St")
        db.session.add_all([pizza, restaurant])
        db.session.commit()

        with pytest.raises(ValueError):
            restaurant_pizza = RestaurantPizza(
                restaurant_id=restaurant.id, pizza_id=pizza.id, price=0
            )
            db.session.add(restaurant_pizza)
            db.session.commit()

    def test_price_too_high(self):
        """Fails when price is above 30."""

        pizza = Pizza(name=Faker().name(), ingredients="Dough, Sauce, Cheese")
        restaurant = Restaurant(name=Faker().name(), address="Main St")
        db.session.add_all([pizza, restaurant])
        db.session.commit()

        with pytest.raises(ValueError):
            restaurant_pizza = RestaurantPizza(
                restaurant_id=restaurant.id, pizza_id=pizza.id, price=31
            )
            db.session.add(restaurant_pizza)
            db.session.commit()
