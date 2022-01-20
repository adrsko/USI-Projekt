import os
import uuid
from main import db, Cars, User

db.create_all()

filename = os.path.join(os.path.dirname(__file__), 'lol.txt')
with open(filename, encoding='utf8') as f:
    data = f.read().splitlines()
    while data[0] != "\n":
        car = Cars(id = str(uuid.uuid4()), brand=data[0], model=data[1], year=int(data[2]), price=int(data[3]), transmission=data[4], mileage=int(data[5]), fuel_type=data[6])
        db.session.add(car)
        db.session.commit()
        for i in range(7):
            del data[0]