import html
from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

#Database configuration 
app.config['MYSQL_HOST'] = '156.67.73.51'
app.config['MYSQL_USER'] = 'u359363630_ignition'
app.config['MYSQL_PASSWORD'] = '2;rRRya0yH'
app.config['MYSQL_DB'] = 'u359363630_ignition'

mysql = MySQL(app)



@app.route('/')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

@app.route('/event')
def event():
    return render_template('event.html')

@app.route('/alerts')
def alerts():
    return render_template('alerts.html')


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

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    print(rv)

    return render_template('admin/job-form.html')



#post a job form by a company
@app.route('/admin/job-list')
def listpostjob():

    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM job')
    rv = cursor.fetchall()

    print(rv)

    return render_template('admin/job-list.html')


#Show applications list 
@app.route('/admin/my-applications')
def myapplications():
    #cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM application')
    #rv = cursor.fetchall()
    return render_template('admin/applications.html')



#Show applications list 
@app.route('/admin/my-profile')
def myprofile():
    #cursor = mysql.connection.cursor()
    #cursor.execute('SELECT * FROM application')
    #rv = cursor.fetchall()
    return render_template('admin/profile-candidate.html')



if __name__ == '__main__':
    app.run(debug=True)