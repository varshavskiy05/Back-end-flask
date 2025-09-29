# myapp/models.py
import datetime

# In-memory "база"
users = {}
categories = {}
records = {}

# Счётчики ID
user_counter = 1
category_counter = 1
record_counter = 1



def create_user(name: str):
    global user_counter
    user = {"id": user_counter, "name": name}
    users[user_counter] = user
    user_counter += 1
    return user


def create_category(name: str):
    global category_counter
    category = {"id": category_counter, "name": name}
    categories[category_counter] = category
    category_counter += 1
    return category


def create_record(user_id: int, category_id: int, amount: float):
    global record_counter
    record = {
        "id": record_counter,
        "user_id": user_id,
        "category_id": category_id,
        "created_at": datetime.datetime.utcnow().isoformat(),
        "amount": amount
    }
    records[record_counter] = record
    record_counter += 1
    return record
