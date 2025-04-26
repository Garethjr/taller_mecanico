from database import db
from datetime import date
from datetime import datetime

class Client(db.Model):

    __tablename__= "clients"

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(40),nullable=True)
    email = db.Column(db.String(200),unique=True,nullable=True)
    phone = db.Column(db.String(20),unique=True,nullable=True)
    birthdate = db.Column(db.String(40), nullable=True)

    def __init__(self,name,email,phone,birthdate):

        self.name = name
        self.email = email
        self.phone = phone
        self.birthdate = datetime.strptime(birthdate,"%Y/%m/%d").date()
    
    #funcion para sacar la edad
    def get_age(self):

        if self.birthdate:

            today = date.today()#guardamos la fecha de hoy

            age = today.year-self.birthdate.year

            if(today.month,today.day)<(self.birthdate.month,self.birthdate.day):#saber si ya cumplió años
                age-=1

            return age
        
        return None
    
    def serialize(self):

        return{
            "name": self.name,
            "email":self.email,
            "phone":self.phone,
            "age":self.get_age()
        }