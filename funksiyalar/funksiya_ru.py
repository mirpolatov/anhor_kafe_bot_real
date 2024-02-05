import random

from db import Session, FoodItem, Ichimliklar, Salat, SalatRu, IchimliklarRu, FoodItemRu


def get_selected_food_name_ru():
    session = Session()
    food_items = session.query(FoodItemRu).all()

    if food_items:
        available_food_names = [food_item.food_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None


def get_selected_ichimlik_name_ru():
    session = Session()
    food_items = session.query(IchimliklarRu).all()

    if food_items:
        available_food_names = [food_item.ichimlik_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None


def get_selected_salat_name_ru():
    session = Session()
    food_items = session.query(SalatRu).all()

    if food_items:
        available_food_names = [food_item.salat_name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None
