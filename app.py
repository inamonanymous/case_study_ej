from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from model import db, Patient, Appointments, Admin, Services, Staff
from sqlalchemy import desc
from mailer import sendMessage
import datetime
from flask_migrate import Migrate

app = Flask(__name__)
app.secret_key = "secret+key"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost:3306/dentistry'
db.init_app(app)
Migrate(app, db)

@app.route('/client-signout', methods=['GET'])
def client_signout():
    session.clear()
    return redirect(url_for('client_page'))
    
    
@app.route('/client-signin', methods=['POST'])
def client_signin():
    email, password = request.form['email'], request.form['password']
    if Patient.login_is_true(email, password):
        session['patient-email'] = email
        return redirect(url_for('client_page'))
    return redirect(url_for('client_page'))

@app.route('/delete-patient/<int:id>', methods=['DELETE', 'GET'])
def delete_patient(id):
    if 'admin-username' in session:
        target_patient = Patient.query.filter_by(patient_id=id).first()
        if not (target_patient):
            return jsonify({"message": "patient or appointment not found"}), 401
        db.session.delete(target_patient)
        db.session.commit()
        return jsonify({"message": "patient deleted"}), 201
    return redirect(url_for('admin_dashboard'))

@app.route('/schedule-appointment', methods=['POST', 'GET'])
def schedule_appointment():
    current_patient = Patient.query.filter_by(email=session.get('patient-email', "")).first()
    if current_patient:
        date, time = request.form['date'], request.form['time']
        timestamp_str = f"{date} {time}"
        timestamp = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M")
        appointment_obj = Appointments.query.filter_by(appointment_date=timestamp.date(), status=1).first()
        if appointment_obj or timestamp < datetime.datetime.today():
            return """  <script>
                            alert("Please make sure the date is not on Doctors Calendar or ahead of the current date");
                            window.location.href="/patient-schedule";
                         </script>"""
        appointment_entry = Appointments(
            patient_id=current_patient.patient_id,
            admin_id=None,
            appointment_date=date,
            appointment_time=time,
            status=0
        )
        db.session.add(appointment_entry)
        db.session.commit()
        return """  <script>
                        alert("Apointment added, kindly wait for the doctors response through your email or contact number for approval, Thank you!");
                        window.location.href="/client-page";
                    </script>"""
        
    return """  
                <script>
                    alert("Please Log in First");
                    history.back();
                </script>"""
    
@app.route('/registration-page', methods=['GET'])
def registration_page():
    return render_template('patient-registration.html')

@app.route('/patient-registration', methods=['POST', 'GET'])
def patient_registration():
    firstname, lastname, age, gender, phone, email, address, password, password2 = request.form['firstname'].strip(), request.form['lastname'].strip(), request.form['age'].strip(), request.form['gender'].strip(), request.form['phone'].strip(), request.form['email'].strip(), request.form['address'].strip(), request.form['password'].strip(), request.form['password2'].strip()
    check_patient = Patient.query.filter_by(email=email).first()
    if check_patient:
        return f"""
            <script>
                alert("Email already Registered");
                history.back();
            </script>
            """    
    if password!=password2:
        return f"""
            <script>
                alert("Password doesn't match!");
                history.back();
            </script>
            """    

    patient_entry = Patient(
        firstname=firstname,
        lastname=lastname,
        age=age,
        gender=gender,
        contact_number=phone,
        email=email,
        address=address,
        password=password
    )
    db.session.add(patient_entry)
    db.session.commit()
    return f"""
            <script>
                alert("Patient successfully Registered!");
                window.location.href='/client-page';
            </script>
            """

@app.route('/get-service-description/<int:id>')
def get_service_description(id):
    target_service = Services.query.filter_by(service_id=id).first()
    if not target_service:
        return jsonify({"message": "object not found"}), 401
    
    return jsonify({"description": target_service.service_description}), 201

@app.route('/client-page')
def client_page():
    all_appointments = Appointments.query.order_by(desc(Appointments.appointment_id)).all()
    approved_appointments = Appointments.query.filter_by(status=1).all()
    completed_appointments = Appointments.query.filter_by(status=2).all()
    services = Services.query.all()
    if 'patient-email' in session:
        current_patient = Patient.query.filter_by(email=session.get('patient-email', "")).first()
        current_patient_history = Appointments.query.filter_by(patient_id=current_patient.patient_id).all()
        return render_template('client-page.html',
                                current_patient=current_patient,
                                all_appointments=current_patient_history, 
                                approved_appointments=approved_appointments,
                                completed_appointments=completed_appointments,
                                services=services)
    return render_template('client-page.html',
                            current_patient=None,
                            all_appointments=None, 
                            approved_appointments=approved_appointments,
                            completed_appointments=completed_appointments,
                            services=services)

#admin logic
#-------------------------------------------------------------------------------------
@app.route('/admin-edit-service/<int:id>', methods=['PUT'])
def admin_edit_service(id):
    if 'admin-username' in session:
        target_service = Services.query.filter_by(service_id=id).first()
        data = request.get_json()
        target_service.service_title=data.get(f"input-title-{id}")
        target_service.service_description=data.get(f"input-description-{id}")
        target_service.service_price=data.get(f"input-price-{id}")
        db.session.commit()
        return jsonify(data)
    return redirect(url_for('index'))

@app.route('/admin-delete-service/<int:id>', methods=['DELETE'])
def admin_delete_service(id):
    if 'admin-username' in session:
        target_service = Services.query.filter_by(service_id=id).first()
        if not target_service:
            return redirect(url_for('index')), 401
        db.session.delete(target_service)
        db.session.commit()
        return jsonify({"message": "service deleted"}), 200
    return redirect(url_for('index'))

@app.route('/admin-save-service', methods=['POST', 'GET'])
def admin_save_sevice():
    if 'admin-username' in session:
        title, description, price = request.form['title'].strip(), request.form['description'], request.form['price'].strip()
        check_service = Services.query.filter_by(service_title=title).first()
        if check_service:
            return """      <script>
                                alert("Cannot add existing Service");
                                window.location.href="/admin-dashboard";
                            </script>
                    """

        service_entry = Services(
            service_title=title,
            service_description=description,
            service_price=price
        )
        db.session.add(service_entry)
        db.session.commit()
        return redirect(url_for('admin_dashboard'))
    return redirect(url_for('index'))

@app.route('/admin-edit-admin/<int:id>', methods=['PUT', 'GET'])
def admin_edit_admin(id):
    if 'admin-username' in session:
        data = request.get_json()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_admin.staff_id).first()
        target_admin = Admin.query.filter_by(admin_id=id).first()
        if not data:
            print(data)
            return jsonify({"message": "null data"}), 401
        if not (current_staff.position == 0 or current_staff.position == 1 or not current_admin.staff_id == id):
            return jsonify({"message": "hierarchy not followed"}), 401
        if not data['password'] == data['password2']:
            return jsonify({"message": "password do not match"}), 401
        target_admin.username=data['username']
        target_admin.password=data['password']
        session['admin-username'] = target_admin.username
        db.session.commit()
        return jsonify(data), 201
    return redirect(url_for('index'))

@app.route('/admin-edit-current-staff', methods=['POST', 'GET'])
def admin_edit_current_staff():
    if 'admin-username' in session:
        data = request.get_json()
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        target_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        if not data:
            return jsonify({"message": "null data"})
        target_staff.firstname=data['firstname']
        target_staff.lastname=data['lastname']
        target_staff.contact_number=data['phone']
        target_staff.email=data['email']
        db.session.commit()
        print(data)
        return jsonify({"message": data}), 201
    return redirect(url_for('index'))

@app.route('/admin-edit-staff/<int:id>', methods=['POST', 'GET'])
def admin_edit_staff(id):
    if 'admin-username' in session:
        data = request.get_json()
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        target_staff = Staff.query.filter_by(staff_id=id).first()
        if not data:
            return jsonify({"message": "null data"}), 401
        if not (current_staff.position == 0 or current_staff.position == 1 or not current_user.staff_id == id):
            return jsonify({"message": "hierarchy not followed"}), 401
        target_staff.firstname=data['firstname']
        target_staff.lastname=data['lastname']
        target_staff.position=data['position']
        target_staff.contact_number=data['phone']
        target_staff.email=data['email']
        db.session.commit()
        print(data)
        return jsonify({"message": data}), 201
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
        if (current_staff.position == 0 or current_staff.position == 1) and (not target_staff.position == 0):
            db.session.delete(target_staff)
            db.session.delete(target_admin)
            db.session.commit()
            return jsonify({"message": "success"}), 200
        return jsonify({"message": "cannot delete | position hierarchy not followed"}), 413
    return redirect(url_for('index'))

@app.route('/admin-get-staff/<int:id>')
def admin_get_staff(id):
    if 'admin-username' in session:
        target_staff = Staff.query.filter_by(staff_id=id).first()
        target_admin = Admin.query.filter_by(staff_id=id).first()
        if not target_admin and not target_staff:
            return jsonify({"message": "staff not found"}), 413
        data = {
            "firstname": target_staff.firstname,
            "lastname": target_staff.lastname,
            "position": target_staff.position,
            "phone": target_staff.contact_number,
            "email": target_staff.email,
        }
        return jsonify(data)
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

            return f"""
                    <script>
                        alert("Staff saved successfully! New Staff's Username: {username.strip()} | Password: {lastname.strip()}");
                        window.location.href="/admin-dashboard";
                    </script>
                    """
        return f"""
                    <script>
                        alert("Hirarchy not followed, Staff saved unsuccessfully!");
                        location.reload(true);
                    </script>
                    """
    return redirect(url_for('index'))

@app.route('/admin-delete-appointment/<int:id>', methods=['DELETE'])
def admin_delete_appointment(id):
    if 'admin-username' in session:
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        if (target_appointment.status<=1 or target_appointment.status>=0) and current_admin:
            db.session.delete(target_appointment)
            db.session.commit()
            return jsonify({"message": "appointment deleted"}), 201
        return jsonify({"message": "failed"}), 401
    return redirect(url_for('index'))


@app.route('/admin-complete-appointment/', methods=['PUT'])
def admin_complete_appointment():
    if 'admin-username' in session:
        data = request.get_json()
        id = data['id']
        service = data['service']
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        target_patient = Patient.query.filter_by(patient_id=target_appointment.patient_id).first()
        if target_appointment.status==1 and current_admin:
            target_appointment.status=2
            target_appointment.admin_id=current_admin.admin_id
            target_appointment.service_id=service
            target_patient.is_verified=1
            db.session.commit()
            return jsonify({"message": "appointment status set to completed"}), 201
        return jsonify({"message": "failed"}), 401
    return redirect(url_for('index'))

@app.route('/admin-approve-appointment/<int:id>', methods=['PUT'])
def admin_approve_appointment(id):
    if 'admin-username' in session:
        target_appointment = Appointments.query.filter_by(appointment_id=id).first()
        if target_appointment is None: 
            return jsonify({"message": "not found"}), 401    
        current_admin = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        if target_appointment.status==0 and current_admin:
            current_patient = Patient.query.filter_by(patient_id=target_appointment.patient_id).first()
            sendMessage(current_patient, target_appointment.appointment_date, target_appointment.appointment_time)
            target_appointment.status=1
            target_appointment.admin_id=current_admin.admin_id
            db.session.commit()
            return jsonify({"message": "appointment status set to approved"}), 201
        return jsonify({"message": "failed"}), 401
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin-username' in session:
        current_user = Admin.query.filter_by(username=session.get('admin-username', "")).first()
        current_staff = Staff.query.filter_by(staff_id=current_user.staff_id).first()
        patients_obj = Patient.query.order_by(desc(Patient.patient_id)).all()
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
                                services_obj=services_obj
                                )
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
@app.route('/patient/<int:id>')
def view_patient(id):
    if 'admin-username' in session:
        patient = Patient.query.filter_by(patient_id=id).first()
        data = {
            "firstname": patient.firstname,
            "lastname": patient.lastname,
            "age": patient.age,
            "gender": patient.gender,
            "contact_number": patient.contact_number,
            "email": patient.email,
            "address": patient.address,
            "is_verified": patient.is_verified
        }
        return jsonify(data)
    return "<script>alert('RESTRICTED ACCESS');window.location.href='/';</script>"

@app.route("/api/appointments")
def appointments_api():
    # Fetch your appointments from the database
    approved_appointments = Appointments.query.filter_by(status=1).all()
    # Convert them to the JSON structure expected by FullCalendar
    appointments_json = [
        {
            'title': f'Appointment with ID {appointment.appointment_date}',
            'start': f'{appointment.appointment_date}T{appointment.appointment_time}',
        
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
    app.run(host="0.0.0.0", port="5000", debug=True)