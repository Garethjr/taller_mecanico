# Importamos la instancia de base de datos.
from database import db
from datetime import date

# Definimos el modelo Client.
class Client(db.Model):
    __tablename__="clients"  # Nombre de la tabla en la base de datos.

# Columnas de la tabla con sus tipos de datos.
    id = db.column(db.Integer, primary_key =True)
    name = db.column(db.String(50), nullable =True)
    email = db.column(db.String(200), unique =True, nullable =True)
    phone = db.column(db.String(20), unique =True, nullable =True)
    birthdate = db.column(db.Date, nullable =True)

    # Constructor para inicializar los atributos del cliente
    def __init__(self, name, email, phone, birtdhate):
        self.name = name
        self.email = email
        self.phone = phone
        self.birthdate = birtdhate

    # Método para calcular la edad del cliente
    def get_age(self):
        if self.birthdate:
            today = date.today() # Fecha actual
            age = today.year - self.birthdate.year
            if (today.month,today.day) < (self.birthdate.month,self.birthdate.day): # Saber si ya cumplió años
                age-=1 # Si todavía no cumplió años este año
            return age
        return None # Si ingresa fecha de nacimiento, no se puede calcular la edad
    
    # Método para convertir el objeto a un diccionario (esto sirve enviar como JSON)
    def serialize(self):
        return{
            "id":self.id,
            "name": self.name,
            "email":self.email,
            "phone":self.phone,
            "birthdate":self.birthdate.isoformate() if self.birthdate else None, # Convierta la fecha de nacimiento en un texto con formato estándar (AAAA-MM-DD) si existe; si no, devuelve None.
            "age":self.get_age()
        }