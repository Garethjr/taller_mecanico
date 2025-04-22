from sqlalchemy.exc import IntegrityError
from flask import Blueprint, jsonify, request
from database import db
from models.client import Client

client=Blueprint("client",__name__)

@client.route("/api/client")
def get_client():
    clients = Client.query.all()#Devuelve una lista de objetos clientes
    return jsonify([client.serialize() for client in clients])#convertirlo en formato jsonify

@client.route("/api/add_client",methods=["POST"])

def add_client():
    datos_db=request.get_json()#convierte en diccionario
    if not datos_db or not all(key in datos_db for key in ['name', 'email', 'phone',"birthdate"]):
        return jsonify({'--ERROR--': 'faltan datos'}), 400
    try:
        print(f"Datos recibidos: {datos_db}")  

        new_client = Client(datos_db['name'], datos_db['email'], datos_db['phone'],datos_db["birtdate"])
        print(f"Creando cliente: {new_client.name}, {new_client.email}, {new_client.phone},{new_client.birthdate}")

        db.session.add(new_client)#agrega el nuevo cliente al area de preparacion
        db.session.commit()#confirma y guarda ese cambio a la base de datos

        return jsonify({'mensaje': 'Cliente agregado exitosamente', 'cliente': new_client.serialize()}), 201#fue creado con exito
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'email exitente'}), 400
    
    except Exception as e:#Guarda errores y te lo muestra
        db.session.rollback()
        return jsonify({"Error inesperado": str(e)}),500

@client.route("/api/client_delete",methods=["Delete"])
def client_del():
    id=request.get_json(id)#Obtener el id manualmente
    client = Client.query.get(id)
    
    if not client: 
        return jsonify({'Mensaje':'No se encontro el cliente'}), 404 
    try:
        db.session.delete(client)
        db.session.commit()
        return jsonify({'Mensaje': '--Cliente eliminado--'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'Error inesperado':str(e)}), 500

@client.route("/api/cliente_Put",methods=["Put"])
def update_cliente(id):
    id=request.get_json(id)
    data_db = request.get_json()

    if not data_db:
        return jsonify({'error':'No se recibieron datos'}, 400)
    
    client = Client.query.get(id)

    if not client:
        return jsonify({'error': 'Cliente no encontrado'}), 404
    
    try:
        if "name" in data_db:
            client.name = data_db['name']
        if 'email' in data_db:
            client.email = data_db['email']
        if 'phone' in data_db:
            client.phone = data_db['phone']
        if "birthdate" in data_db:
            client.birthdate = data_db[" birthdate"]

        db.session.commit()

        return jsonify({'mensaje':'Cliente actulizado correctamente', 'cliente': client.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
    

@client.route("/api/Patch_client",methods=["Patch"])
def client_patch():
    id=request.get_json(id)
    data_db=request.get_json()
    cleint=Client.query.get(id)

    if data_db == False:
        return jsonify({"error": "No se encontraron datos"}),404
    if client == False:
        return jsonify({"error": "No se encontró el cleinte"}),404
    
    
    try:
        if "name" in data_db:
            client.name = data_db['name']
        if 'email' in data_db:
            client.email = data_db['email']
        if 'phone' in data_db:
            client.phone = data_db['phone']
        if "birthdate" in data_db:
            client.birthdate = data_db[" birthdate"]
        db.session.commit()

        return jsonify({'mensaje':'Cliente actulizado correctamente', 'cliente': client.serialize()}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
