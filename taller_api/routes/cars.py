from flask import Blueprint, request, jsonify
from models.Cars import Car
from database.db import db

vehiculo_bp = Blueprint('vehiculo_bp', __name__)

@vehiculo_bp.route('/', methods=['POST'])
def crear_vehiculo():
    data = request.json
    nuevo = Vehiculo(marca=data['marca'], modelo=data['modelo'], patente=data['patente'], cliente_id=data['cliente_id'])
    db.session.add(nuevo)
    db.session.commit()
    return jsonify({"mensaje": "Vehículo creado"}), 201

@vehiculo_bp.route('/', methods=['GET'])
def obtener_vehiculos():
    vehiculos = Vehiculo.query.all()
    resultado = [{"id": v.id, "marca": v.marca, "modelo": v.modelo, "patente": v.patente, "cliente_id": v.cliente_id} for v in vehiculos]
    return jsonify(resultado)

@vehiculo_bp.route('/<int:id>', methods=['PUT'])
def actualizar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    data = request.json
    vehiculo.marca = data.get('marca', vehiculo.marca)
    vehiculo.modelo = data.get('modelo', vehiculo.modelo)
    vehiculo.patente = data.get('patente', vehiculo.patente)
    db.session.commit()
    return jsonify({"mensaje": "Vehículo actualizado"})

@vehiculo_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_vehiculo(id):
    vehiculo = Vehiculo.query.get_or_404(id)
    db.session.delete(vehiculo)
    db.session.commit()
    return jsonify({"mensaje": "Vehículo eliminado"})