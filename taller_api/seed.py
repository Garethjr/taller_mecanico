import json
from datetime import datetime
from flask import Flask
from database import db
from models.client import Client
from models.car import Car
from models.repair import Repair 
from models.mechanic import Mechanic
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
        
         # Cargamos los mecanicos del archivo JSON
        with open("data_json/datos_mechanic.json", encoding="utf-8") as file:
            mechanics_data = json.load(file)
            for mech in mechanics_data:
                if not Mechanic.query.filter_by(phone=mech["phone"]).first():
                    new_mech = Mechanic(
                        name=mech["name"],
                        specialty=mech["specialty"],
                        phone=mech["phone"]
                    )
                    db.session.add(new_mech)
            db.session.commit()
            print("--Datos de mecánicos cargados--")

        # Cargamos las reparaciones del archivo JSON
        with open("data_json/datos_repair.json", encoding="utf-8") as file:
            repairs_data = json.load(file)

            for repair in repairs_data:
                # Evitamos duplicados por combinación de car_id y mechanic_id en esa fecha
                existing_repair = Repair.query.filter_by(
                    car_id=repair["car_id"],
                    mechanic_id=repair["mechanic_id"],
                    date=repair["date"]
                ).first()

                if not existing_repair:
                    new_repair = Repair(
                        description=repair["description"],
                        date=repair["date"],
                        cost=repair["cost"],
                        car_id=repair["car_id"],
                        mechanic_id=repair["mechanic_id"]
                    )
                    db.session.add(new_repair)

            db.session.commit()
            print("--Datos de reparaciones cargados--")
            
    except Exception as e:
        db.session.rollback() # Cancela todo si hay un error
        print(f"Error al cargar datos: {e}")