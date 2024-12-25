import bcrypt
from extension import db
from datetime import datetime,timezone

class User(db.Model):
    __tablename__ = "user"
    
    u_id = db.Column(db.Integer,primary_key=True)
    role = db.Column(db.String(20),nullable=False) 
    email = db.Column(db.String(100),unique=True, nullable=False)
    profile_picture_name = db.Column(db.String(50))
    profile_picture = db.Column(db.LargeBinary)
    password = db.Column(db.String(100), nullable=False)


    def set_password(self,password):
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
    household = db.relationship('Household')


class Household(db.Model):
    __tablename__ = "household"
    
    h_id = db.Column(db.Integer, db.ForeignKey("user.u_id"), primary_key=True,autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    state = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(500), nullable=False)



class ServiceProfessional(db.Model):
    __tablename__ = "service_professional"
    
    s_id = db.Column(db.Integer, db.ForeignKey('user.u_id'), primary_key=True, autoincrement = True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    phone_number = db.Column(db.String(15), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    about = db.Column(db.String(500))
    ser_id = db.Column(db.Integer, db.ForeignKey('service.ser_id'), nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    rating = db.Column(db.Float,default = 0.0)
    state = db.Column(db.String(30), nullable=False)
    city = db.Column(db.String(30), nullable=False)
    pin_code = db.Column(db.String(10), nullable=False)
    address = db.Column(db.String(500), nullable=False)
    age = db.Column(db.Integer,nullable = False)
    price = db.Column(db.Integer)
    document_name = db.Column(db.String(50))
    document = db.Column(db.LargeBinary)
    
    appointment = db.relationship('Service',back_populates='professional')
        
   
class Service(db.Model):
    __tablename__ = "service"
    
    ser_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    desc = db.Column(db.String(200))
    base_price = db.Column(db.Integer)
        
    request = db.relationship('Request',back_populates='service')
    professional = db.relationship('ServiceProfessional',back_populates='appointment')
    


class Request(db.Model):
    __tablename__ = "request"
    
    req_id = db.Column(db.Integer, primary_key=True)
    payment_type = db.Column(db.String(50), nullable=False)
    payment_id = db.Column(db.String(100), unique=True)
    rating = db.Column(db.Integer)
    s_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    ser_id = db.Column(db.Integer,db.ForeignKey('service.ser_id'))
    h_id = db.Column(db.Integer, db.ForeignKey('user.u_id'))
    comments = db.Column(db.String(500))
    date_req = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    date_comp = db.Column(db.DateTime)
    status = db.Column(db.String(50))
    
    service = db.relationship('Service',back_populates='request')

  

class Cart(db.Model):
    __tablename__ = "cart"
    
    cart_id = db.Column(db.Integer, primary_key=True)
    h_id = db.Column(db.Integer, db.ForeignKey("household.h_id"))
    s_id = db.Column(db.Integer, db.ForeignKey("service_professional.s_id"))
