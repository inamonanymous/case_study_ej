from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patient'
    patient_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(7), nullable=False)
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    address = db.Column(db.String(100), nullable=False)
    treatment = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    is_verified = db.Column(db.Boolean, default=0)

    @classmethod
    def login_is_true(cls, email, password):
        patient_obj = cls.query.filter_by(email=email).first()
        return patient_obj and patient_obj.password == password

class Admin(db.Model):
    __tablename__ = 'admin'
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    staff_id = db.Column(db.Integer, nullable=False)

    @classmethod
    def login_is_true(cls, username, password):
        admin_obj = cls.query.filter_by(username=username).first()
        return admin_obj and admin_obj.password == password


class Appointments(db.Model):
    __tablename__ = 'appointments'
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    admin_id = db.Column(db.Integer)
    appointment_date = db.Column(db.Date, nullable=False)
    appointment_time = db.Column(db.Time, nullable=False)
    status = db.Column(db.SmallInteger, comment="0-pending, 1-approved, 2-completed")
    

class Staff(db.Model):
    __tablename__ = 'staff'
    staff_id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100), nullable=False)
    lastname = db.Column(db.String(100), nullable=False)
    position = db.Column(db.SmallInteger, comment="0-master, 1-dentist, 2-hygienist, 3-receiptionist")
    contact_number = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)

class Services(db.Model):
    __tablename__ = 'services'
    service_id = db.Column(db.Integer, primary_key=True)
    service_title = db.Column(db.String(100), nullable=False)
    service_description = db.Column(db.String(255), nullable=False)
    service_price = db.Column(db.Float)