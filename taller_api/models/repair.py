from database.db import db
class Repair (db.Model):
    _tablename_ = 'repair'
    id = db.Column(db.Integer, primary_key=True)
    descripcion = db.Column(db.String(200), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    costo = db.Column(db.Float, nullable=False)

    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)