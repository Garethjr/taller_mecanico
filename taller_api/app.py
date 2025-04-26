from flask import Flask
from config import DATABASE_URL 
from database import db
from models import Client, Car
from routes.clients import clients_bp
from routes.cars import car_bp
from routes.repairs import repair_bp
from routes.mechanic import mechanic_bp
from models import repair

app = Flask(__name__) # Crea la app de Flask

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False


# Iniciamos la base de datos
db.init_app(app)

# Registramos los blueprints

app.register_blueprint(clients_bp)
app.register_blueprint(car_bp)
app.register_blueprint(repair_bp)
app.register_blueprint(mechanic_bp)
#@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)