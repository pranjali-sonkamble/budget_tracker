import json
from budget import Category

FILE_NAME = "budget_data.json"


def save_data(categories: dict):
    data = {}
    for name, category in categories.items():
        data[name] = category.ledger

    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


def load_data():
    categories = {}

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

        for name, ledger in data.items():
            category = Category(name)
            category.ledger = ledger
            categories[name] = category

    except FileNotFoundError:
        pass

    return categories
