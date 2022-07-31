import pyrebase
from flask import render_template, request, redirect, session,url_for,flash
import os
import html
import yaml
from functools import wraps
from flask import Flask, render_template
from flask_mysqldb import MySQL


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'


#Load configuration file from yaml file
with open('db_config.yml', 'r') as file:
    db_config = yaml.safe_load(file)

with open('firebase_config.yml', 'r') as file:
    firebase_config = yaml.safe_load(file)
print(db_config['database'])

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

#Show a list of job on the frontend
@app.route('/jobs')
def jobs():
    #request to get the jobs
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    result = cursor.fetchall()
    cursor.close()
    return render_template('jobs.html', jobs = result)

#Show a list of job for a particular company on the front
@app.route('/jobs/<int:job_id>')
def jobs_company(job_id):
    #request to get the jobs
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job AS J LEFT JOIN company AS C ON J.company_id = C.id WHERE C.id =' + str(job_id) )
    result = cursor.fetchall()
    cursor.close()
    return render_template('jobs.html', jobs = result)

#Page to show the job description
@app.route('/job-description/<int:job_id>')
def jobdescription(job_id):

    #request to get the jobs
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job WHERE id=' + str(job_id)  )
    result = cursor.fetchone()
    print(result)
    return render_template('job-description.html', job = result)



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

            print("Email => " + email)
            print("PAWD : " + password)
            try:
                
                print("Try to connect")
                if( auth.sign_in_with_email_and_password(email, password) ): # In case this is successfull
                    #Store user information into session
                    print("Starting SQL query")
                    cursor = mysql.connection.cursor()
                    cursor.execute("SELECT * from user where email=%s and password=%s",(email,password))
                    data = cursor.fetchone()

                    print("data => ")
                    print(data)

                    if data:
                        session['logged_in']=True
                        session['user_id']= data["id"]
                        session['username']=data["name"]
                        session['email']=data["email"]
                        session['role']=data["role"]
                        session['company_id']=data["company_id"]
                

                return render_template('home.html')

            except:
                unsuccessful = 'Please check your credentials'
                return render_template('login.html', umessage=unsuccessful)
    return render_template('login.html')# once loged in stays here(create log out)

@app.route('/createaccount', methods=['GET', 'POST'])
def createaccount():
    if (request.method == 'POST'):
            email = request.form['name']
            password = request.form['password']
            
            if (auth.create_user_with_email_and_password(email, password) ):
                print("Info User")
                print(password)

                cur=mysql.connection.cursor()
                cur.execute("INSERT INTO user(password,email, role) VALUES(%s,%s,%s)",( password,email, "CANDIDATE"))
                mysql.connection.commit()

                #Save information in session
                session['email']=email
                #session['user_id']=1

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
 
#Login mysql
@app.route('/loginemp',methods=['POST','GET'])
def loginemp():
    status=True
    if request.method=='POST':
        email=request.form["email"]
        pwd=request.form["upass"]
        print(pwd)
        cur=mysql.connection.cursor()
        cur.execute("SELECT * from user where EMAIL=%s and PASSWORD=%s",(email,pwd))
        data=cur.fetchone()
        if data:
            session['logged_in']=True
            session['username']=data["name"]
            flash('Login Successfully','success')
            return redirect('admin')
        else:
            flash('Invalid Login. Try Again','danger')
    return render_template("loginemp.html")

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('loginemp'))
	return wrap
  
#Registration  
@app.route('/reg',methods=['POST','GET'])
def reg():
    status=False
    print(request)

    if request.method=='POST':
        name=request.form["uname"]
        email=request.form["email"]
        pwd=request.form["upass"]

        print(pwd)

        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO user(name,password,email, role) VALUES(%s,%s,%s, %s)",(name,pwd,email, "RECRUITER"))
        mysql.connection.commit()

        cur.close()
        flash('Registration Successfully. Login Here...','success')
        return redirect('admin')
    return render_template("reg.html",status=status)

#Home page
#@app.route("/home")
#@is_logged_in
#def home():
	#return render_template('home.html')
    
#logout end o gmysql log in/out
@app.route("/logout")
def logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('login'))


#Admin Home page
@app.route('/admin')
def admin():

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
    cursor.execute('SELECT * FROM job WHERE company_id=' + str(session["company_id"]) )
    rv = cursor.fetchall()
    return render_template('admin/job-list.html', job = rv)

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
        date_str = dt[0] +"-"+ dt[1] + "-"+ dt[2] + " 00:00:00" #datetime of expiration 2022-07-28 12:00:01
           
        
        #Atempt to Insert Job inside the database
        cursor = mysql.connection.cursor()
        sql_req = """INSERT INTO job (title, location, jobtype, company_id, expiration, description) 
                                    VALUES (%s, %s, %s, %s, %s, %s)"""
        data = (title, location, jobtype, company_id, date_str, description)
        cursor.execute(sql_req, data)
        cursor.close()
        print("MySQL connection is closed")
    
    return listpostjob()

#Show applications list of the Candidate
@app.route('/admin/my-applications')
def myapplications():
    candidate_id=1 # We should get the candidate id from the session
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM application WHERE candidate_id = ' + str(candidate_id) )
    #cursor.execute(sql_req, data)
    result = cursor.fetchall()
    print(result)

    return render_template('admin/applications.html', applications=result)

#Show candidate applications by a recruiter 
@app.route('/admin/applications/<int:job_id>')
def applications(job_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM application WHERE job_id = ' + str(job_id) )
    #cursor.execute(sql_req, data)
    result = cursor.fetchall()
    print(result)

    for item in result:
        print(item)

    return render_template('admin/applications.html', applications=result)


'''
#Show applications list of the Candidate
@app.route('/admin/company')
def company():
    candidate_id = session['user_id'] # Get the candidate id from the session
    
    if session['company_id'] != None:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM company WHERE id =' + str(session['company_id']) )
        #cursor.execute(sql_req, data)
        result = cursor.fetchall()
        print("Company Defined =>")
        print(result)

    return render_template('admin/company.html', applications=result)
'''

#Show profile information 
@app.route('/admin/my-profile')
def myprofile():
    #cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM application')
    #rv = cursor.fetchall()
    return render_template('admin/profile-candidate.html')

#Show List of companies on front end page  
@app.route('/companies')
def companies():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM company')
    data = cursor.fetchall()
    return render_template('companies.html', companies = data)

#Show company of the recruiter 
@app.route('/admin/company', methods = ['POST', 'GET'])
def mycompany():
    
    if request.method == 'GET': #Show the form
        #Take company of the connected user
        print("=> Try get company")

        company = None
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM company WHERE id='"+ str(session["company_id"])+"'" )
        data = cursor.fetchone()

        if(data):
            print("Company of the user")
            print(data)

            return render_template('admin/company.html', company = data )

    
    if request.method == 'POST':
        #Get input from form

        name = request.form.get("name")
        location = request.form.get("location")
        email = request.form.get("email")
        #logo = session['company_id'] #We assign the company id of the connected user
        description = request.form.get("description")

        #Create or Update a company
        cursor = mysql.connection.cursor()

        if(session["company_id"] <= 0): #not defined
            data = (name, location, email, description)
            sql_req = """INSERT INTO company (name, location, email, description) 
                                    VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql_req, data)
            print("=> Insert")
            company_id_inserted = cursor.lastrowid

            #Assign company ID to the user
            sql_update = """UPDATE user SET company_id =%s WHERE id =%s"""
            data = (company_id_inserted, session["user_id"])
            cursor.execute(sql_update, data)

        else:
            data = (name, location, email, description, str(session["company_id"]))
            sql_req = """UPDATE company SET name = %s, location= %s, email= %s, description= %s WHERE id=%s"""
            cursor.execute(sql_req, data)

        #print(cursor.insert_id())

        cursor.close()


        return redirect('/admin/company')




#Show Application form
@app.route('/apply/<int:job_id>')
def apply(job_id):

    #request to get job description

    return render_template('apply.html')


if __name__ == '__main__':
    app.run(debug=True)