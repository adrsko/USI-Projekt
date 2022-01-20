from main import db, Cars

db.create_all()

query2 = db.session.query(Cars.model.distinct().label("model")).filter_by(brand='BMW')
brands2 = [row.model for row in query2.all()]
print(brands2)