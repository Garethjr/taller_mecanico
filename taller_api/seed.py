import json
from datetime import datetime
from flask import Flask
from database import db
from models.client import Client
from models.car import Car
from app import app
from sqlalchemy import or_
# Iniciamos el contexto de la app para que SQLAlchemy pueda trabajar con la base de datos.
with app.app_context():
    try:
        # Cargamos clientes desde el archivo json
        with open ("data_json/datos_client.json", encoding="utf-8") as file:
            clients_data = json.load(file) # Convertimos el JSON en una lista de diccionarios

            for client in clients_data:
                # Verificamos si ya hay un cliente con ese correo.
                if not Client.query.filter(or_(
                    (Client.email == client["email"]) | (Client.phone == client["phone"])
                )).first():
                    # Creamos un nuevo cliente y lo agregamos a la base de datos
                    new_client = Client(
                        name =client["name"],
                        email =client["email"],
                        phone =client["phone"],
                        birthdate =datetime.strptime(client["birthdate"], "%Y-%m-%d").date()
                    )
                    db.session.add(new_client) # Preparamos al cliente para ser agreagado a la base de datos
            db.session.commit() # Guardamos los cambios en la base de datos
            print("--Datos del cliente cargados--")

            # Cargamos los autos del archivo json
        with open("data_json/datos_car.json", encoding="utf-8") as file:
            cars_data = json.load(file)

            for car in cars_data:
                # Verificamos si hay un auto con esa patente
                if not Car.query.filter_by(license_plate=car["license_plate"]).first():
                    # Creamos un nuevo auto y lo agregamos a la base de datos
                    new_car = Car(
                        brand = car["brand"],
                        model = car["model"],
                        year = car["year"],
                        license_plate = car["license_plate"],
                        client_id = car["client_id"],
                    )
                    db.session.add(new_car) # Preparamos el auto para ser agreagado a la base de datos
            
            db.session.commit() # Guardamos los cmabios en la base de datos
            print("Los datos fueron cargados correctamente")

    except Exception as e:
        db.session.rollback() # Cancela todo si hay un error
        print(f"Error al cargar datos: {e}")