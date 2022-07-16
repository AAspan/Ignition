"#Job-Board-Application" 
A simple Project For helping people to find a job quickly.
After Installation you need to update your virtual environmen path

Requirements:
You need to install python 3

VIRTUAL_ENV="__"
cd to the directory where requirements.txt is located.

When you have python installed,
in command line, you enter the project folder you have clonned from github.

#Then Activate the virtual environment with the below command:
> venv\Scripts\activate


#Install the packages with pip:
> pip install -r requirements.txt

#if you can't install pycrypto it is okay.
#pycryptodome is compatible with the same code as pycrypto.
#You might need to install pycryptodome with the next command
> pip install pycryptodome


#if MySQL is not installed, you can install it with the following command
> pip install flask_mysqldb

#if yaml is not installed, you can install it by the following command
> pip3 install PyYAML


#To Run the Application you can do 
> python -m flask run

#or if flask is in your environement path, you can do
> flask run