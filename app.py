from flask import Flask, render_template, request, redirect, url_for, session
from model import db, Patient, Appointments, Admin, Staff

app = Flask(__name__)
app.secret_key = "secret+key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dentistry'
db.init_app(app)

@app.route('/schedule-appointment', methods=['POST', 'GET'])
def schedule_appointment():
    if 'patient-id' in session:
        current_patient = Patient.query.filter_by(patient_id=session.get('patient-id')).first()
        if current_patient:
            date, time = request.form['date'], request.form['time']
            appointment_entry = Appointments(
                patient_id=current_patient.patient_id,
                admin_id=None,
                appointment_date=date,
                appointment_time=time,
                status=0
            )
            db.session.add(appointment_entry)
            db.session.commit()
            return f"appointment sent to admin {appointment_entry}"
        return redirect(url_for('client_page'))
    return redirect(url_for('client_page'))

@app.route('/patient-schedule/')
def patient_schedule():
    if 'patient-id' in session:
        
        
        return render_template('schedule-appointment.html')
    return redirect(url_for('client_page'))
        
@app.route('/patient-registration', methods=['POST', 'GET'])
def patient_registration():
    treatment, firstname, lastname, age, gender, phone, email, address = request.form['treatment'], request.form['firstname'], request.form['lastname'], request.form['age'], request.form['gender'], request.form['phone'], request.form['email'], request.form['address'], 
    patient_entry = Patient(
        firstname=firstname,
        lastname=lastname,
        age=age,
        gender=gender,
        contact_number=phone,
        email=email,
        address=address,
        treatment=treatment
    )
    db.session.add(patient_entry)
    db.session.commit()
    session['patient-id'] = patient_entry.patient_id
    return redirect(url_for('patient_schedule'))

@app.route('/client-page')
def client_page():
    all_appointments = Appointments.query.all()
    print(all_appointments)
    return render_template('client-page.html', all_appointments=all_appointments)

#admin logic
#-------------------------------------------------------------------------------------

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        return render_template('admin-dashboard.html', current_user=current_user)
    return redirect(url_for('index'))

@app.route('/admin-auth', methods=['POST', 'GET'])
def admin_auth():
    if request.method == "POST":
        username, password = request.form['username'], request.form['password']
        if Admin.login_is_true(username, password):
            session['admin-username'] = username
            return redirect(url_for('admin_dashboard'))
        return redirect(url_for('index'))
    return redirect(url_for('index'))

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)