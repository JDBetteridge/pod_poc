import os

from csv import DictWriter
from datetime import datetime
from glob import glob
from pathlib import Path

fieldnames = ["timestamp", "order"]

def mk_log_dir():
    os.makedirs("log", exist_ok=True)

def log_delivery(order_number):
    now = datetime.now()
    filename = f"{now.date().isoformat()}_delivery_log.csv"
    path = os.path.join("log", filename)

    if not os.path.isfile(path):
        with open(path, 'w') as csvfile:
            writer = DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

    with open(path, 'a') as csvfile:
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow({"timestamp": datetime.now().isoformat(), "order": order_number})

def get_log():
    path = os.path.join(os.getcwd(), "log", "*.csv")
    return [Path(f) for f in glob(path)]
