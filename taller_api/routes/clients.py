from flask import Blueprint, request, jsonify
from sqlalchemy.exc import IntegrityError
from database import db
from models.client import Client

client = Blueprint("client", __name__)

# Obtener todos los clientes
@client.route("/api/client", methods=["GET"])
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])

# Agregar un cliente nuevo
@client.route("/api/add_client", methods=["POST"])
def add_client():
    datos_db = request.get_json()

    if not datos_db or not all(key in datos_db for key in ['name', 'email', 'phone', 'birthdate']):
        return jsonify({'--ERROR--': 'faltan datos'}), 400

    try:
        print(f"Datos recibidos: {datos_db}")  

        new_client = Client(
            datos_db['name'],
            datos_db['email'],
            datos_db['phone'],
            datos_db['birthdate']
        )

        print(f"Creando cliente: {new_client.name}, {new_client.email}, {new_client.phone}, {new_client.birthdate}")

        db.session.add(new_client)
        db.session.commit()

        return jsonify({'mensaje': 'Cliente agregado exitosamente', 'cliente': new_client.serialize()}), 201

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Email o teléfono ya registrados"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"Error inesperado": str(e)}), 500

# Eliminar un cliente
@client.route("/api/client_delete/<int:id>", methods=["DELETE"])
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"mensaje": "Cliente no encontrado"}), 404

    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'Mensaje': '--Cliente eliminado--'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'Error inesperado': str(e)}), 500

# Actualizar todos los datos del cliente (PUT)
@client.route("/api/cliente_Put/<int:id>", methods=["PUT"])
def update_cliente(id):
    data_db = request.get_json()
    if not data_db:
        return jsonify({'error': 'No se recibieron datos'}), 400

    client = Client.query.get(id)
    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404

    try:
        client.name = data_db.get("name", client.name)
        client.email = data_db.get("email", client.email)
        client.phone = data_db.get("phone", client.phone)
        client.birthdate = data_db.get("birthdate", client.birthdate)

        db.session.commit()
        return jsonify({'mensaje': 'Cliente actualizado correctamente', 'cliente': client.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# Actualizar parcialmente (PATCH)
@client.route("/api/Patch_client/<int:id>", methods=["PATCH"])
def client_patch(id):
    data_db = request.get_json()
    client = Client.query.get(id)

    if not client:
        return jsonify({"mensaje": "Cliente no encontrado"}), 404

    try:
        if "name" in data_db and data_db["name"]:
            client.name = data_db['name']
        if 'email' in data_db and data_db["email"]:
            client.email = data_db['email']
        if 'phone' in data_db and data_db["phone"]:
            client.phone = data_db['phone']
        if "birthdate" in data_db and data_db["birthdate"]:
            client.birthdate = data_db["birthdate"]

        db.session.commit()
        return jsonify({'mensaje': 'Cliente actualizado correctamente', 'cliente': client.serialize()}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
