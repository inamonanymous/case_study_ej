from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from model import db, Patient, Appointments, Admin, Services, Staff
from flask_migrate import Migrate
from sqlalchemy import desc
import json

app = Flask(__name__)
app.secret_key = "secret+key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/dentistry'
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/schedule-appointment', methods=['POST', 'GET'])
def schedule_appointment():
    if 'patient-id' in session:
        current_patient = Patient.query.filter_by(patient_id=session.get('patient-id')).first()
        if current_patient:
            date, time = request.form['date'], request.form['time']
            appointment_obj = Appointments.query.filter_by(appointment_date=date, status=1).first()
            if appointment_obj:
                return "schedule different date"
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
    all_appointments = Appointments.query.order_by(desc(Appointments.appointment_id)).all()
    approved_appointments = Appointments.query.filter_by(status=1).all()
    completed_appointments = Appointments.query.filter_by(status=2).all()
    services = Services.query.all()
    return render_template('client-page.html',
                            all_appointments=all_appointments, 
                            approved_appointments=approved_appointments,
                            completed_appointments=completed_appointments,
                            services=services)

#admin logic
#-------------------------------------------------------------------------------------
@app.route('/admin-edit-staff/<int:id>', methods=['POST', 'GET'])
def admin_edit_staff(id):
    if 'admin-username' in session:
        data = request.get_json()
        if not data:
            return jsonify({"message": "null data"})
        target_staff = Staff.query.filter_by(staff_id=id).first()
        target_staff.firstname=data['firstname']
        target_staff.lastname=data['lastname']
        target_staff.position=data['position']
        target_staff.contact_number=data['phone']
        target_staff.email=data['email']
        db.session.commit()
        
        return jsonify({"message": request.get_json()})
    return redirect(url_for('index'))

@app.route('/admin-delete-staff/<int:id>')
def admin_delete_staff(id):
    if 'admin-username' in session:
        target_staff = Staff.query.filter_by(staff_id=id).first()
        target_admin = Admin.query.filter_by(staff_id=id).first()
        if not target_admin and not target_staff:
            return jsonify({"message": "staff not found"}), 413
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        if (current_staff.position == 0 or current_staff.position == 1) and (not target_staff.position == 0) :
            db.session.delete(target_staff)
            db.session.delete(target_admin)
            db.session.commit()
            return jsonify({"message": "success"}), 200
        return jsonify({"message": "cannot delete | position hierarchy not followed"}), 413
    return redirect(url_for('index'))

@app.route('/admin-save-staff', methods=['POST'])
def admin_save_staff():
    if 'admin-username' in session:
        firstname, lastname, position, phone, email, username = request.form['firstname'], request.form['lastname'], int(request.form['position']), request.form['phone'], request.form['email'], request.form['username']
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        check_current_admin = Admin.query.filter_by(username=username.strip()).first()
        if (current_staff.position == 0 or current_staff.position == 1) and (not check_current_admin):
            staff_entry = Staff(
                firstname=firstname.strip(),
                lastname=lastname.strip(),
                position=position,
                contact_number=phone.strip(),
                email=email
            )
            db.session.add(staff_entry)
            db.session.commit()

            admin_entry = Admin(
                username=username.strip(),
                password=lastname.strip(),
                staff_id=staff_entry.staff_id
            )

            db.session.add(admin_entry)
            db.session.commit()

            return f"success {staff_entry.firstname} -- {admin_entry.username}"
        return "f"
    return redirect(url_for('index'))

@app.route('/admin-delete-appointment/<int:id>')
def admin_delete_appointment(id):
    if 'admin-username' in session:
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        if (target_appointment.status<=1 or target_appointment.status>=0) and current_admin:
            db.session.delete(target_appointment)
            db.session.commit()
            return redirect(url_for('admin_dashboard'))
        return "faileed"
    return redirect(url_for('index'))


@app.route('/admin-complete-appointment/<int:id>')
def admin_complete_appointment(id):
    if 'admin-username' in session:
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        if target_appointment.status==1 and current_admin:
            target_appointment.status=2
            target_appointment.admin_id=current_admin.admin_id
            db.session.add(target_appointment)
            db.session.commit()
            return "success"
        return "faileed"
    return redirect(url_for('index'))

@app.route('/admin-approve-appointment/<int:id>')
def admin_approve_appointment(id):
    if 'admin-username' in session:
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        if target_appointment.status==0 and current_admin:
            target_appointment.status=1
            target_appointment.admin_id=current_admin.admin_id
            db.session.add(target_appointment)
            db.session.commit()
            return "success"
        return "failed"
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        patients_obj = Patient.query.all()
        appointments_obj = Appointments.query.order_by(desc(Appointments.appointment_id)).all()
        pending_appointments_obj = Appointments.query.filter_by(status=0).order_by(desc(Appointments.appointment_id)).all()
        approved_appointments_obj = Appointments.query.filter_by(status=1).order_by(desc(Appointments.appointment_id)).all()
        completed_appointments_obj = Appointments.query.filter_by(status=2).order_by(desc(Appointments.appointment_id)).all()
        staffs_obj = Staff.query.all()
        services_obj = Services.query.all()

        return render_template('admin-dashboard.html',
                                current_user=current_user, 
                                current_staff=current_staff,
                                patients_obj=patients_obj,
                                appointments_obj=appointments_obj,
                                pending_appointments_obj=pending_appointments_obj,
                                approved_appointments_obj=approved_appointments_obj,
                                completed_appointments_obj=completed_appointments_obj,
                                staffs_obj=staffs_obj,
                                services_obj=services_obj)
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


#api logic
#-------------------------------------------------------------------------------------
@app.route('/appointment/<int:appointment_id>')
def view_appointment(appointment_id):
    appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
    return f"{appointment.appointment_date}"

@app.route("/api/appointments")
def appointments_api():
    # Fetch your appointments from the database
    approved_appointments = Appointments.query.filter_by(status=1).all()
    # Convert them to the JSON structure expected by FullCalendar
    appointments_json = [
        {
            'title': f'Appointment with ID {appointment.appointment_id}',
            'start': f'{appointment.appointment_date}T{appointment.appointment_time}',
            'url': f'/appointment/{appointment.appointment_id}',
            # any other event properties...
        }
        for appointment in approved_appointments  # Assume approved_appointments is a list of appointments
    ]
    return jsonify(appointments_json)


@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0",debug=True)