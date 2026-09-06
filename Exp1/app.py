from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)
app.secret_key = 'xyzsdfg'

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'chandana'   # Change to your MySQL password
app.config['MYSQL_DB'] = 'mydb'

mysql = MySQL(app)


# ---------------- LOGIN ----------------
@app.route('/')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(
            'SELECT * FROM user WHERE email=%s AND password=%s',
            (email, password)
        )

        user = cursor.fetchone()

        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['name'] = user['name']
            session['email'] = user['email']

            return render_template('user.html', message="Logged in Successfully!")

        else:
            message = "Incorrect Email or Password!"

    return render_template('login.html', message=message)


# ---------------- REGISTER ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''

    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute(
            'SELECT * FROM user WHERE email=%s',
            (email,)
        )

        account = cursor.fetchone()

        if account:
            message = "Account already exists!"

        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = "Invalid Email Address!"

        elif not name or not email or not password:
            message = "Please fill all fields!"

        else:
            cursor.execute(
                'INSERT INTO user(name,email,password) VALUES(%s,%s,%s)',
                (name, email, password)
            )

            mysql.connection.commit()

            message = "Registration Successful!"

    return render_template('register.html', message=message)


# ---------------- USER PAGE ----------------
@app.route('/user')
def user():
    if 'loggedin' in session:
        return render_template('user.html')
    return redirect(url_for('login'))


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():

    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('name', None)
    session.pop('email', None)

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)