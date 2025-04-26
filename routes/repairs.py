
# Importaciones necesarias
from flask import Blueprint, request, jsonify  # Para definir rutas, recibir datos del cliente y responder en formato JSON
from models.repair import Repair               # Modelo de la tabla "repair"
from database import db                     # Objeto que representa la base de datos SQLAlchemy
from datetime import datetime                  # Para convertir cadenas de texto en fechas

# Creamos un Blueprint llamado 'repair_bp' para agrupar todas las rutas relacionadas con las reparaciones
repair_bp = Blueprint('repair_bp', __name__)


# Ruta para crear una nueva reparación (POST /repair/)

@repair_bp.route('/api/Post repair', methods=['POST'])
def create_repair():
    data = request.json  # Obtenemos los datos enviados en el cuerpo de la solicitud (formato JSON)
    new_repair = Repair(  # Creamos una instancia del modelo Repair con los datos recibidos
        description=data['description'],
        date=datetime.strptime(data['date'], '%Y-%m-%d'),  # Convertimos el string de fecha a objeto datetime
        cost=data['cost'],
        car_id=data['car_id']
    )
    db.session.add(new_repair)  # Agregamos la reparación a la sesión de la base de datos
    db.session.commit()         # Confirmamos los cambios en la base de datos
    return jsonify({"mensaje": "Reparación creada"}), 201  # Respondemos con mensaje de éxito



# Ruta para obtener todas las reparaciones (GET /repair/)
@repair_bp.route('/api/Get repair', methods=['GET'])
def get_repairs():
    repairs = Repair.query.all()  # Traemos todas las reparaciones desde la base de datos
    result = [  # Recorremos cada una para armar una lista de diccionarios con los datos necesarios
        {
            "id": r.id,
            "description": r.description,
            "date": r.date.isoformat(),  # Convertimos la fecha a formato string ISO
            "cost": r.cost,
            "car_id": r.car_id
        }
        for r in repairs
    ]
    return jsonify(result)  # Devolvemos la lista como respuesta JSON

# Ruta para eliminar una reparación (DELETE /repair/<id>)
@repair_bp.route('/<int:id>', methods=['DELETE'])
def delete_repair(id):
    repair = Repair.query.get_or_404(id)  # Buscamos la reparación por ID o devolvemos 404 si no existe
    db.session.delete(repair)  # Marcamos el objeto para eliminación
    db.session.commit()        # Confirmamos la eliminación
    return jsonify({"mensaje": "Reparación eliminada"})  # Mensaje de éxito

