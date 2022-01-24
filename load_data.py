import os
import uuid
from main import db, Cars, User

db.create_all()

filename = os.path.join(os.path.dirname(__file__), 'cars_list.txt')
with open(filename, encoding='utf8') as f:
    data = f.read().splitlines()
    while data[0] != "\n":
        print(data[0], data[1], data[2], data[3], data[4], data[5])
        car = Cars(id = str(uuid.uuid4()), model=data[0], year=int(data[1]), price=int(data[2]), transmission=data[3], mileage=int(data[4]), fuel_type=data[5])
        db.session.add(car)
        db.session.commit()
        for i in range(6):
            del data[0]