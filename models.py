from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Patient(db.Model):
    __tablename__ = 'patients'
    PatientID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    Gender = db.Column(db.String(10))
    PhoneNumber = db.Column(db.String(15))
    Address = db.Column(db.String(100))
    Zipcode = db.Column(db.String(10))
    ContactPersonName = db.Column(db.String(50))
    ContactPersonPhoneNumber = db.Column(db.String(15))
    PaymentInformation = db.Column(db.String(100))
    PasswordHash = db.Column(db.String(128))

class Physician(db.Model):
    __tablename__ = 'physicians'
    
    PhysicianID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(50), nullable=False)
    LastName = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(120), nullable=False, unique=True)
    Gender = db.Column(db.String(10))
    PhoneNumber = db.Column(db.String(15))
    Address = db.Column(db.String(100))
    Zipcode = db.Column(db.String(10))
    Availability = db.Column(db.String(50))
    Specialty = db.Column(db.String(50))
    PhysicianRank = db.Column(db.String(50))
    HospitalAttached = db.Column(db.String(100))
    PasswordHash = db.Column(db.String(128))

class Service(db.Model):
    __tablename__ = 'services'
    
    ServiceID = db.Column(db.Integer, primary_key=True)
    ServiceName = db.Column(db.String(50), nullable=False)
    ServiceDescription = db.Column(db.String(255))
    ServiceCost = db.Column(db.Float)
    PhysicianID = db.Column(db.Integer, db.ForeignKey('physicians.PhysicianID'))

class BillingRate(db.Model):
    __tablename__ = 'billing_rates'
    
    BillingRateID = db.Column(db.Integer, primary_key=True)
    PhysicianRank = db.Column(db.String(50))
    HourlyRate = db.Column(db.Float)

"""class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer, db.ForeignKey('patients.PatientID'))
    PhysicianID = db.Column(db.Integer, db.ForeignKey('physicians.PhysicianID'))
    Date = db.Column(db.Date)
    Time = db.Column(db.Time)
    AmountBilled = db.Column(db.Float)"""
    
class Appointment(db.Model):
    __tablename__ = 'appointments'

    AppointmentID = db.Column(db.Integer, primary_key=True)
    PatientID = db.Column(db.Integer)  # Assuming this will be retrieved from the session or database
    PatientFirstName = db.Column(db.String(50), nullable=False)
    PatientLastName = db.Column(db.String(50), nullable=False)
    PatientAddress = db.Column(db.String(100), nullable=False)
    PhysicianID = db.Column(db.Integer, db.ForeignKey('physicians.PhysicianID'), nullable=False)
    PhysicianFirstName = db.Column(db.String(50), nullable=False)
    PhysicianLastName = db.Column(db.String(50), nullable=False)
    Date = db.Column(db.Date, nullable=False)
    Time = db.Column(db.Time, nullable=False)
    AmountBilled = db.Column(db.Float)


# Function to get a patient by email
def get_patient_by_email(email):
    return Patient.query.filter_by(email=email).first()

# Function to get a physician by email
def get_physician_by_email(email):
    return Physician.query.filter_by(email=email).first()