from flask import Flask, request, session, redirect, url_for, render_template
import mysql.connector
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField
from datetime import datetime, timedelta
import Database

app = Flask(__name__)
app.secret_key = 'App@1234'

# DataBase Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'BLOGGINGPLATFORM'
}

# Register User
@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = sha256_crypt.hash(request.form['password'])
        email = request.form['email']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

# Checking if username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username,password))

        existing_user = cursor.fetchone()
        if existing_user:
            return "Username or email already exists!"

# Insert new user into databases
        cursor.execute("INSERT INTO users(username,password,email) VALUES(%s, %s, %s)",(username,password,email))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))
    
    return render_template('register.html')

# User login
@app.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['username']

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Retrieve user from database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and sha256_crypt.verify(password, user[2]):  # Verify hashed password
            session['logging_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        
        else:
            return "Invalid username or password!"
        
    return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard (Protected Route)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f"Welcome (session['username'])! You are logged in."
    
    else:
        return redirect(url_for('login'))
    
  

if '_name_' == '_main_':
    app.run(debug=True,port=8080)
