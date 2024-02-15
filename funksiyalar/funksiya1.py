import random

from db import Session, MainMenu, Menu


def get_selected_food_name():
    session = Session()
    food_items = session.query(MainMenu).all()

    if food_items:
        available_food_names = [food_item.name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None


def get_selected_food_name2():
    session = Session()
    food_items = session.query(Menu).all()

    if food_items:
        available_food_names = [food_item.name for food_item in food_items]
        selected_food_name = random.choice(available_food_names)
        return selected_food_name
    else:
        return None
