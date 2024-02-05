import random

from db import Session, FoodItem, Ichimliklar, Salat


def get_selected_food_name():
    session = Session()
    food_items = session.query(FoodItem).all()

    if food_items:
        available_food_names = [food_item.food_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None


def get_selected_ichimlik_name():
    session = Session()
    food_items = session.query(Ichimliklar).all()

    if food_items:
        available_food_names = [food_item.ichimlik_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None


def get_selected_salat_name():
    session = Session()
    food_items = session.query(Salat).all()

    if food_items:
        available_food_names = [food_item.salat_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None
