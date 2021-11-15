import requests
import pytest
import json
import os
import uuid
from main import db, Cars, User

db.create_all()

filename = os.path.join(os.path.dirname(__file__), 'test.txt')
with open(filename, encoding='utf8') as f:
    data = f.readlines()
    while data[0] != "\n":
        car = Cars(id = str(uuid.uuid4()), brand=data[0], model=data[1], year=int(data[2]), mileage=int(data[3]), price=int(data[4]))
        db.session.add(car)
        db.session.commit()
        for i in range(5):
            del data[0]