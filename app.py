import pyrebase
from flask import render_template, request, redirect, session
import os
import html
from flask import Flask, render_template

config = {
    "apiKey": "",
    "authDomain": "",
    "databaseURL": "",
    "projectId": "",
    "storageBucket": "",
    "messagingSenderId": "",
    "appId": ""
}
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')
#Authentication


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            try:
                auth.sign_in_with_email_and_password(email, password)
                return render_template('client.html')
            except:
                unsuccessful = 'Please check your credentials'
                return render_template('profile.html', umessage=unsuccessful)
    return render_template('profile.html')# once loged in stays here(create log out)

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
            return render_template('profile.html')
    return render_template('forgotpassword.html')

@app.route('/client', methods=['GET', 'POST'])
def client():
    return render_template('client.html')

if __name__ == '__main__':
    app.run(debug=True)