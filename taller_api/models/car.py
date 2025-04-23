from database import db

class Vehiculo(db.Model):

    _tablename_ = 'vehiculos'
    
    id = db.Column(db.Integer, primary_key=True)
    marca = db.Column(db.String(50), nullable=False)
    modelo = db.Column(db.String(50), nullable=False)
    patente = db.Column(db.String(20), unique=True, nullable=False)

    cliente_id = db.Column(db.Integer, db.ForeignKey('clientes.id'), nullable=False)

    # Relación: un vehículo puede tener muchas reparaciones
    reparaciones = db.relationship('Reparacion', backref='vehiculo', cascade='all, delete')
