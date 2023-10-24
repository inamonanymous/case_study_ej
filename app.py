from flask import Flask, render_template, request, redirect

app = Flask(__name__)

@app.route('/patient-registration', methods=['POST', 'GET'])
def patient_registration():
    treatment, firstname, lastname, age, gender, phone, email, address = request.form['treatment'], request.form['firstname'], request.form['lastname'], request.form['age'], request.form['gender'], request.form['phone'], request.form['email'], request.form['address'], 
    return f"{(treatment, firstname, lastname, age, gender, phone, email, address)}"

@app.route('/admin-login')
def admin_login():
    return render_template('admin-login.html')

@app.route('/client-page')
def client_page():
    return render_template('client-page.html')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)