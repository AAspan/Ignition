import pyrebase
from flask import render_template, request, redirect, session
import os
import html
from flask import Flask, render_template
from flask_mysqldb import MySQL

app = Flask(__name__)
#Database configuration 
app.config['MYSQL_HOST'] = '156.67.73.51'
app.config['MYSQL_USER'] = 'u359363630_ignition'
app.config['MYSQL_PASSWORD'] = '2;rRRya0yH'
app.config['MYSQL_DB'] = 'u359363630_ignition'

mysql = MySQL(app)
config = {
    "apiKey": "AIzaSyAdd9FxfkdRtucyyGCY0ShlyklvzyqrdRs",
    "authDomain": "ignition-1bf3e.firebaseapp.com",
    "databaseURL": "https://ignition-1bf3e-default-rtdb.firebaseio.com/",
    "projectId": "ignition-1bf3e",
    "storageBucket": "ignition-1bf3e.appspot.com",
    "messagingSenderId": "74076369865",
    "appId": "1:74076369865:web:ffd34b99a10b0a08236e18"
}

@app.route('/')
def homelog():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')
#Authentication


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                return render_template('hometwo.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')# once loged in stays here(create log out)

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            auth.create_user_with_email_and_password(email, password)
            return render_template('profile.html')
    return render_template('createaccount.html')

@app.route('/forgotpassword', methods=['GET', 'POST'])
def forgotpassword():
    if (request.method == 'POST'):
            email = request.form['name']
            auth.send_password_reset_email(email)
            return render_template('login.html')
    return render_template('forgotpassword.html')

@app.route('/hometwo', methods=['GET', 'POST'])
def hometwo():
    return render_template('hometwo.html')
    
#Admin
@app.route('/admin')
def admin():

    #if request.method == 'GET':
    #    return "Login via the login Form"

    #name = request.form['name']
    #age = request.form['age']

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    #return str(rv)

    return render_template('admin/index.html')



#post a job
@app.route('/admin/postjob')
def formpostjob():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    return render_template('admin/post_job.html')

#Dashboard
@app.route('/admin/dashboard')
def dashboard():
    title = "Dashboard"
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    return render_template('admin/dashboard.html', title = title)

if __name__ == '__main__':
    app.run(debug=True)