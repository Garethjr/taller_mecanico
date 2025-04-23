from flask import Blueprint, request, jsonify
from models.repair import Repairs
from database import db
from datetime import datetime

reparacion_bp = Blueprint('reparacion_bp', __name__)

@reparacion_bp.route('/', methods=['POST'])
def crear_reparacion():
    data = request.json
    nueva = Repairs(
        descripcion=data['descripcion'],
        fecha=datetime.strptime(data['fecha'], '%Y-%m-%d'),
        costo=data['costo'],
        vehiculo_id=data['vehiculo_id']
    )
    db.session.add(nueva)
    db.session.commit()
    return jsonify({"mensaje": "Reparación creada"}), 201

@reparacion_bp.route('/', methods=['GET'])
def obtener_reparaciones():
    reparaciones = Repairs.query.all()
    resultado = [{"id": r.id, "descripcion": r.descripcion, "fecha": r.fecha.isoformat(), "costo": r.costo, "vehiculo_id": r.vehiculo_id} for r in reparaciones]
    return jsonify(resultado)

@reparacion_bp.route('/<int:id>', methods=['PUT'])
def actualizar_reparacion(id):
    reparacion = Repairs.query.get_or_404(id)
    data = request.json
    reparacion.descripcion = data.get('descripcion', reparacion.descripcion)
    reparacion.costo = data.get('costo', reparacion.costo)
    reparacion.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d') if 'fecha' in data else reparacion.fecha
    db.session.commit()
    return jsonify({"mensaje": "Reparación actualizada"})

@reparacion_bp.route('/<int:id>', methods=['DELETE'])
def eliminar_reparacion(id):
    reparacion = Repairs.query.get_or_404(id)
    db.session.delete(reparacion)
    db.session.commit()
    return jsonify({"mensaje": "Reparación eliminada"})

