# Importa la instancia de SQLAlchemy desde el archivo database.py
from database import db

# Define la clase Car como un modelo de base de datos
class Car(db.Model):
    __tablename__ = 'cars'

    # Columna 'id' como clave primaria, tipo entero
    id = db.Column(db.Integer, primary_key=True)

    # Columna 'brand' para la marca del auto, tipo string, no puede ser nulo
    brand = db.Column(db.String(100), nullable=False)

    # Columna 'model' para el modelo del auto, tipo string, no puede ser nulo
    model = db.Column(db.String(100), nullable=False)

    # Columna 'license_plate' para la matrícula, debe ser única y no nula
    license_plate = db.Column(db.String(20), unique=True, nullable=False)

    # Columna 'client_id' como clave foránea, enlaza con la tabla 'clients'
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)

    # Relación con el modelo Client (relación uno a muchos)
    # Permite acceder al cliente dueño del auto a través de la propiedad 'client'
    client = db.relationship('Client', back_populates='cars')

    # Método que convierte el objeto Car en un diccionario (útil para APIs JSON)
    def serialize(self):
        return {
            'id': self.id,
            'brand': self.brand,
            'model': self.model,
            'license_plate': self.license_plate,
            'client_id': self.client_id
        }
