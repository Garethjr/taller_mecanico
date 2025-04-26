from datetime import datetime
from database import db

class Repair(db.Model):
    __tablename__ = 'repair'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    date = db.Column(db.Date, nullable=True)
    cost = db.Column(db.Float, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanic.id"), nullable=True)

    def __init__(self, description, date, cost, car_id, mechanic_id):
        self.description = description
        self.date = datetime.strptime(date, "%Y/%m/%d").date()
        self.cost = cost
        self.car_id = car_id
        self.mechanic_id = mechanic_id

    def serialize(self):
        return {
            "id": self.id,
            "description": self.description,
            "cost": self.cost,
            "date": self.date,
            'car_id': self.car_id,
            "mechanic_id": self.mechanic_id
        }
