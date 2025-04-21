from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from database import db
from models.client import Client

client=Blueprint("client",__name__)

@client.route("/api/clients")
def get_client():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients])

@client.route("/api/add_client",methods=["POST"])

def add_client():
    datos_db=request.get_json()
    if not datos_db or not all(key in datos_db for key in ['name', 'email', 'phone',"birthdate"]):
        return jsonify({'--ERROR--': 'faltan datos'}), 400
    try:
        print(f"Datos recibidos: {datos_db}")  

        new_client = Client(datos_db['name'], datos_db['email'], datos_db['phone'],datos_db["birtdate"])
        print(f"Creando cliente: {new_client.name}, {new_client.email}, {new_client.phone},{new_client.birthdate}")

        db.session.add(new_client)
        db.session.commit()

        return jsonify({'mensaje': 'Cliente agregado exitosamente', 'cliente': new_client.serialize()}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'El email ya está registrado'}), 400