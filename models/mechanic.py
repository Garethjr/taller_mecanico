from database import db

class Mechanic(db.Model):
    __tablename__ = "mechanic"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    specialty = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True, unique=True)
    mechanic_id = db.Column(db.Integer, db.ForeignKey("mechanic.id"),nullable=True)

    def __init__(self, name, specialty=None, phone=None):
        self.name = name
        self.specialty = specialty
        self.phone = phone

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "specialty": self.specialty,
            "phone": self.phone
        }
