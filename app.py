from flask import Flask, render_template, redirect, url_for, session, request, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from models import *  
from flask_migrate import Migrate

from config import Config
import datetime

app = Flask(__name__)
app.config.from_object(Config)


# Initialize the database with the app
db.init_app(app)

# Optionally initialize Flask-Migrate
migrate = Migrate(app, db)

# Test Windows Authentication
def test_db_connection():
    try:
        with app.app_context():
            db.engine.connect()  # Attempt to connect to the database
            print("Connection to the database was successful.")
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register_patient', methods=['GET', 'POST'])
def register_patient():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form["email"]
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']
        zipcode = request.form['zipcode']
        contact_person_name = request.form['contact_person_name']
        contact_person_phone = request.form['contact_person_phone']
        payment_info = request.form['payment_info']
        password = request.form['password']

        # Check if the email already exists
        existing_patient = Patient.query.filter_by(Email=email).first()
        if existing_patient:
            flash('Email already exists. Please sign in.', 'error')
            return redirect(url_for('patient_login'))
        
        # Hash the password
        password_hash = generate_password_hash(password)

        new_patient = Patient(
            FirstName=first_name,
            LastName=last_name,
            Email=email,
            Gender=gender,
            PhoneNumber=phone_number,
            Address=address,
            Zipcode=zipcode,
            ContactPersonName=contact_person_name,
            ContactPersonPhoneNumber=contact_person_phone,
            PaymentInformation=payment_info,
            PasswordHash=password_hash
        )

        db.session.add(new_patient)
        db.session.commit()
        flash('Registration successful! You can now sign in.', 'success')
        return redirect(url_for('patient_login'))

    return render_template('register_patient.html')


@app.route('/login_as_patient', methods=['GET', 'POST'])
def patient_login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Fetch patient from the database
        patient = Patient.query.filter_by(Email=email).first()
        
        # Authentication logic
        if patient and check_password_hash(patient.PasswordHash, password):
            # Store patient info in session
            session['patient_id'] = patient.PatientID
            session['patient_name'] = f"{patient.FirstName} {patient.LastName}"
            flash('Login successful!', 'success')
            return redirect(url_for('patient_dashboard'))  # Redirect to patient dashboard
        else:
            error_message ='Invalid email or password. Please try again.'

    return render_template('login_as_patient.html', error=error_message)

@app.route('/register_physician', methods=['GET', 'POST'])
def register_physician():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form["email"]
        gender = request.form['gender']
        phone_number = request.form['phone_number']
        address = request.form['address']
        zipcode = request.form['zipcode']
        availability = request.form['availability']
        specialty = request.form['specialty']
        physician_rank = request.form['physician_rank']
        hospital_attached = request.form['hospital_attached']
        password = request.form['password']

        # Hash the password
        password_hash = generate_password_hash(password)

        new_physician = Physician(
            FirstName=first_name,
            LastName=last_name,
            Email=email,
            Gender=gender,
            PhoneNumber=phone_number,
            Address=address,
            Zipcode=zipcode,
            Availability=availability,
            Specialty=specialty,
            PhysicianRank=physician_rank,
            HospitalAttached=hospital_attached,
            PasswordHash=password_hash
        )

        db.session.add(new_physician)
        db.session.commit()
        flash('Physician registration successful! You can now sign in.', 'success')
        return redirect(url_for('physician_login'))

    return render_template('register_physician.html')


@app.route('/login_as_physician', methods=['GET', 'POST'])
def physician_login():
    error_message = None
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Fetch physician from the database
        physician = Physician.query.filter_by(Email=email).first()
        
        # Authentication logic
        if physician and check_password_hash(physician.PasswordHash, password):  
            # Store physician info in session
            session['physician_id'] = physician.PhysicianID
            session['physician_name'] = f"{physician.FirstName} {physician.LastName}"
            flash('Login successful!', 'success')
            return redirect(url_for('physician_dashboard'))  # Redirect to physician dashboard
        else:
            error_message ='Invalid email or password. Please try again.'

    return render_template('login_as_physician.html', error=error_message)

# Physician Dashboard
@app.route('/physician_dashboard')
def physician_dashboard():
    physician_id = session.get('physician_id')  # Retrieve physician ID from session
    if not physician_id:
        return redirect(url_for('physician_login'))  # Redirect to login if not logged in

    return render_template('physician_dashboard.html')

# Current Appointments
@app.route('/current_appointments')
def current_appointments():
    physician_id = session.get('physician_id')
    if not physician_id:
        return redirect(url_for('physician_login'))

    current_appts = Appointment.query.filter_by(PhysicianID=physician_id).all()
    return render_template('current_appointments.html', appointments=current_appts)

# Appointment History
@app.route('/appointment_history')
def appointment_history():
    physician_id = session.get('physician_id')
    if not physician_id:
        return redirect(url_for('physician_login'))

    past_appts = Appointment.query.filter(Appointment.PhysicianID == physician_id,
                                          Appointment.Date < datetime.date.today()).all()
    return render_template('appointment_history.html', appointments=past_appts)


# Patient Dashboard
@app.route('/patient_dashboard')
def patient_dashboard():
    patient_id = session.get('patient_id')  # Retrieve patient ID from session
    if not patient_id:
        return redirect(url_for('patient_login'))  # Redirect to login if not logged in

    return render_template('patient_dashboard.html')

# Current Appointments
@app.route('/patient_appointments')
def patient_appointments():
    patient_id = session.get('patient_id')
    if not patient_id:
        return redirect(url_for('patient_login'))

    current_appts = Appointment.query.filter_by(PatientID=patient_id).all()
    return render_template('current_appointments.html', appointments=current_appts)

# Patient Visit History
@app.route('/visit_history')
def visit_history():
    patient_id = session.get('patient_id')
    if not patient_id:
        return redirect(url_for('patient_login'))

    past_appts = Appointment.query.filter(Appointment.PatientID == patient_id,
                                          Appointment.Date < datetime.date.today()).all()
    return render_template('visit_history.html', appointments=past_appts)

@app.route('/search_physician', methods=['GET', 'POST'])
def search_physician():
    error_msg = None
    error_service = None

    if request.method == 'POST':
        zipcode = request.form['zipcode']
        address = request.form['address']
        service_name = request.form['service_name']
        date_required = request.form['date_required']
        time_required = request.form['time_required']

        # Find the service ID based on the service name
        service = Service.query.filter_by(ServiceName=service_name).first()
        
        if not service:
            error_service = 'Service not found.'  # Set error message for service not found
        else:
            # Get the Physician IDs that provide this service
            physicians = Physician.query.filter_by(PhysicianID=service.PhysicianID).all()

            # Filter physicians based on their proximity to the provided zipcode
            matched_physicians = [physician for physician in physicians if physician.Zipcode == zipcode]

            if not matched_physicians:
                error_msg = 'No physicians found matching your criteria.'  # Set error message for no physicians found

        # Render search results if there are no errors
        if not error_msg and not error_service:
            results = [{
                'FirstName': physician.FirstName,
                'LastName': physician.LastName,
                'HospitalAttached': physician.HospitalAttached,
                'DateRequested': date_required,
                'TimeRequested': time_required,
            } for physician in matched_physicians]

            return render_template('search_results.html', results=results)

    return render_template('search_physician.html', error=error_msg, error_service=error_service)


@app.route('/create_appointment', methods=['POST'])
def create_appointment():
    physician_id = request.form['physician_id']
    patient_first_name = request.form['patient_first_name']
    patient_last_name = request.form['patient_last_name']
    patient_address = request.form['patient_address']
    date = request.form['date']
    time = request.form['time']

    # Retrieve the physician details
    physician = Physician.query.get(physician_id)


    service_cost = 100  
    hourly_rate = 30  
    amount_billed = hourly_rate * (1 + service_cost)  # Calculate total billed amount

    new_appointment = Appointment(
        PatientFirstName=patient_first_name,
        PatientLastName=patient_last_name,
        PatientAddress=patient_address,
        PhysicianID=physician.PhysicianID,
        PhysicianFirstName=physician.FirstName,
        PhysicianLastName=physician.LastName,
        Date=date,
        Time=time,
        AmountBilled=amount_billed
    )

    db.session.add(new_appointment)
    db.session.commit()

    return redirect(url_for('current_appointment', appointment_id=new_appointment.AppointmentID))

@app.route('/current_appointment/<int:appointment_id>')
def current_appointment(appointment_id):
    appointment = Appointment.query.get(appointment_id)
    return render_template('current_appointment.html', appointment=appointment)

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))  

if __name__ == '__main__':
    test_db_connection()
    app.run(debug=True)
