# ~ from random import randint

# ~ MIN_ID=1000000
MAX_ID=10000000

def process_form(form):
    item = {}
    item["id"] = hash(form)%MAX_ID
    item["name"] = form["item"]
    item["quantity"] = int(form["quantity"])
    item["price"] = float(form["price"])
    return item
