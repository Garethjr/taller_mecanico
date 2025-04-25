from database import db

class Repair(db.Model):
    __tablename__ = 'repair'  # nombre de la tabla en la base de datos

    id = db.Column(db.Integer, primary_key=True)  # ID único de la reparación
    descripcion = db.Column(db.String(200), nullable=False)  # Descripción de la reparación
    fecha = db.Column(db.Date, nullable=False)  # Fecha de la reparación
    costo = db.Column(db.Float, nullable=False)  # Costo de la reparación

    vehiculo_id = db.Column(db.Integer, db.ForeignKey('vehiculos.id'), nullable=False)  # ID del vehículo asociado
