import pyrebase
from flask import render_template, request, redirect, session
import os
import html
import yaml
from flask import Flask, render_template
from flask_mysqldb import MySQL
import datetime
app = Flask(__name__)

#Load configuration file from yaml file
with open('db_config.yml', 'r') as file:
    db_config = yaml.safe_load(file)

with open('firebase_config.yml', 'r') as file:
    firebase_config = yaml.safe_load(file)


#Database configuration 
app.config['MYSQL_HOST'] = db_config['host']
app.config['MYSQL_USER'] = db_config['user']
app.config['MYSQL_PASSWORD'] = db_config['password']
app.config['MYSQL_DB'] = db_config['database']
mysql = MySQL(app)

config = {
    "apiKey": firebase_config['apiKey'],
    "authDomain": firebase_config['authDomain'],
    "databaseURL": firebase_config['databaseURL'],
    "projectId": firebase_config['projectId'],
    "storageBucket": firebase_config['storageBucket'],
    "messagingSenderId": firebase_config['messagingSenderId'],
    "appId": firebase_config['appId']
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

                #Look inside MySQl, Pull up 
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
        
        if(auth.create_user_with_email_and_password(email, password)):
            
            #Insert the user inside MySQL
            #We can specify the role to make the distinction between candidate and recruiter
            cursor = mysql.connection.cursor()
            sql_req = """INSERT INTO user (email,password) 
                                        VALUES (%s, %s)"""                
            data = (email, password) #Password is not encrypted for now
            cursor.execute(sql_req, data)
            cursor.close()
            print("Registration successful. MySQL connection is closed")

            

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
 

 
#Admin Home page
@app.route('/admin')
def admin():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()
    return render_template('admin/dashboard.html')


#Dashboard
@app.route('/admin/dashboard')
def dashboard():
    title = "Dashboard"
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    return render_template('admin/dashboard.html', title = title)


#post a job form by a company
@app.route('/admin/job-form')
def formpostjob():
    
    return render_template('admin/job-form.html')



#post a job form by a company
@app.route('/admin/job-list')
def listpostjob():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job ')
    rv = cursor.fetchall()

    print(rv)

    return render_template('admin/job-list.html')

#post a job form by a company
@app.route('/admin/add-job', methods = ['POST', 'GET'])
def addjob():

    if request.method == 'GET':
        return formpostjob()


    if request.method == 'POST':
        
        #Get input from form
        title = request.form.get("title")
        location = request.form.get("location")
        jobtype = request.form.get("jobtype")
        company_id = 1 #Will need to come from recruiter company_id
        description = request.form.get("description")
        
        #Treament of the date
        date = request.form.get("expiration_date")
        dt = date.split("-")
        date_str = dt[0] +"-"+ dt[1] + "-"+ dt[2] + " 00:00:00" #datetime of expiration
           
        
        #Atempt to Insert Job inside the database
        cursor = mysql.connection.cursor()
        sql_req = """INSERT INTO job (title, location, jobtype, company_id, expiration, description) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
        data = (title, location, jobtype, company_id, date_str, description)
        cursor.execute(sql_req, data)
        cursor.close()
        print("MySQL connection is closed")
    
    return listpostjob()


#Show applications list 
@app.route('/admin/my-applications')
def myapplications():
    #cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM application')
    #rv = cursor.fetchall()
    return render_template('admin/applications.html')

#Show candidate applications by a recruiter 
@app.route('/admin/applications/<int:job_id>')
def applications(job_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM application WHERE job_id = ' + str(job_id) )
    #cursor.execute(sql_req, data)
    result = cursor.fetchall()
    print(result)
    return "ok"
    #return render_template('admin/applications.html', applications=result)

#Show applications list 
@app.route('/admin/my-profile')
def myprofile():
    #cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM application')
    #rv = cursor.fetchall()
    return render_template('admin/profile-candidate.html')
    

if __name__ == '__main__':
    app.run(debug=True)