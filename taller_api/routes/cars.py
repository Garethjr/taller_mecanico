# Importa funciones necesarias de Flask para crear rutas y manejar peticiones/respuestas
from flask import Blueprint, request, jsonify

# Importa la base de datos y el modelo Car
from database import db
from models.car import Car

# Crea un blueprint para agrupar todas las rutas relacionadas con autos
car_bp = Blueprint('car_bp', __name__)

# Ruta para obtener todos los autos registrados
@car_bp.route('/api/cars', methods=['GET'])
def get_cars():
    # Obtiene todos los objetos Car de la base de datos
    cars = Car.query.all()
    # Retorna una lista de autos convertidos a diccionario (formato JSON)
    return jsonify([car.serialize() for car in cars])

# Ruta para crear un nuevo auto
@car_bp.route('/api/cars', methods=['POST'])
def create_car():
    # Obtiene los datos enviados en formato JSON
    data = request.get_json()

    # Verifica que estén todos los campos requeridos en los datos recibidos
    if not all(key in data for key in ['brand', 'model', 'license_plate', 'client_id']):
        return jsonify({'error': 'Missing car data'}), 400  # Responde con error 400 si falta algo

    # Crea una nueva instancia de Car con los datos recibidos
    new_car = Car(
        brand=data['brand'],
        model=data['model'],
        license_plate=data['license_plate'],
        client_id=data['client_id']
    )

    # Intenta guardar el nuevo auto en la base de datos
    try:
        db.session.add(new_car)      # Agrega el objeto a la sesión
        db.session.commit()          # Guarda los cambios en la base de datos
        return jsonify({'message': 'Car created successfully', 'car': new_car.serialize()}), 201
    except Exception as e:
        db.session.rollback()        # Revierte la transacción en caso de error
        return jsonify({'error': str(e)}), 500  # Responde con error 500 (error interno)

# Ruta para actualizar los datos de un auto existente
@car_bp.route('/api/cars/<int:id>', methods=['PUT'])
def update_car(id):
    # Busca el auto por ID o devuelve un error 404 si no se encuentra
    car = Car.query.get_or_404(id)

    # Obtiene los datos JSON enviados
    data = request.get_json()

    # Actualiza los campos solo si fueron enviados; si no, conserva el valor anterior
    car.brand = data.get('brand', car.brand)
    car.model = data.get('model', car.model)
    car.license_plate = data.get('license_plate', car.license_plate)
    car.client_id = data.get('client_id', car.client_id)

    # Intenta guardar los cambios en la base de datos
    try:
        db.session.commit()  # Confirma los cambios
        return jsonify({'message': 'Car updated successfully', 'car': car.serialize()})
    except Exception as e:
        db.session.rollback()  # Revierte cambios en caso de error
        return jsonify({'error': str(e)}), 500  # Respuesta con error 500

# Ruta para eliminar un auto de la base de datos
@car_bp.route('/api/cars/<int:id>', methods=['DELETE'])
def delete_car(id):
    # Busca el auto por ID o lanza error 404 si no se encuentra
    car = Car.query.get_or_404(id)

    # Intenta eliminar el auto de la base de datos
    try:
        db.session.delete(car)  # Marca el objeto para eliminación
        db.session.commit()     # Confirma la eliminación
        return jsonify({'message': 'Car deleted successfully'})  # Éxito
    except Exception as e:
        db.session.rollback()   # Revierte la transacción si algo falla
        return jsonify({'error': str(e)}), 500  # Error interno del servidor
