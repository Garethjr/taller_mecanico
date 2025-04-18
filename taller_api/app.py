from flask import Flask
from config import DATABASE_URL
from database import db
from models import Client, Car, shift
from routes.clients import clients_bp
from routes.cars import cars_bp
from routes.shifts import shifts_bp

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Iniciamos la base de datos
db.init_app(app)

# Registramos los blueprints

app.register_blueprint(clients_bp)
app.register_blueprint(cars_bp)
app.register_blueprint(shifts_bp)

@app.before_first_request
def create_tables():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)