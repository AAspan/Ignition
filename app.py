import html

from flask import Flask, render_template, request
from flask_mysqldb import MySQL

app = Flask(__name__)

#Database configuration 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ignition'

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