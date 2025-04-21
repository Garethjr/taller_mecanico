from database import db
from datetime import date

class Client(db.Model):
    id=db.column(db.Integer,primary_key=True)
    name=db.column(db.String(20),nullable=True)
    email=db.column(db.String(20),unique=True,nullable=True)
    phone=db.column(db.String(13),unique=True,nullable=True)
    birthdate=db.column(db.Date,nullable=True)

    def __init__(self,name,email,phone,birtdhate):
        self.name=name
        self.email=email
        self.phone=phone
        self.birthdate=birtdhate
    
    def get_age(self):
        if self.birthdate:
            today=date.today()#guardamos la fecha de hoy
            age=today.year-self.birthdate.year
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