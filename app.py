from flask import Flask
from config import DATABASE_URL
from database import db
from models import Client, Car, Repair, Mechanic
from routes.clients import client_bp
from routes.cars import car_bp
from routes.repairs import repair_bp
from routes.mechanic import mechanic_bp

app = Flask(__name__)  # Crea la app de Flask

# Configuración de la base de datos
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicia la base de datos
db.init_app(app)

# Registramos los blueprints
app.register_blueprint(client_bp)
app.register_blueprint(car_bp)
app.register_blueprint(repair_bp)
app.register_blueprint(mechanic_bp)

# Crear las tablas solo cuando la app esté en ejecución
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
