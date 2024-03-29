from flask import Flask, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators
from passlib.hash import sha256_crypt
import mysql.connector

app = Flask(__name__)
app.secret_key = 'App@1234'

# MySQL Configuration
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'BloggingPlatform'
}

# Define User Registration Form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired(), validators.Length(min=6)])
    email = StringField('Email', validators=[validators.InputRequired(), validators.Email()])

# Define User Login Form
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.InputRequired()])
    password = PasswordField('Password', validators=[validators.InputRequired()])

# Register User
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = sha256_crypt.hash(form.password.data)  # Hash the password
        email = form.email.data

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        # Check if username or email already exists
        cursor.execute("SELECT * FROM users WHERE username = %s OR email = %s", (username, email))
        existing_user = cursor.fetchone()
        if existing_user:
            return "Username or email already exists!"

        # Insert new user into database
        cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (username, password, email))
        conn.commit()
        conn.close()

        return redirect(url_for('login'))

    return render_template('register.html', form=form)

# User Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data

        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        print("##########",cursor)
        # Retrieve user from database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username))
        user = cursor.fetchone()
        conn.close()

        if user and sha256_crypt.verify(password, user[2]):  # Verify hashed password
            session['logged_in'] = True
            session['username'] = username
            return render_template('dashboard.html')
        else:
            return "Invalid username or password!"

    return render_template('dashboard.html')

    # return render_template('login.html')

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login.html'))

# Dashboard (Protected Route)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f"Welcome {session['username']}! You are logged in."
    else:
        return redirect(url_for('login.html'))

if __name__ == '__main__':
    app.run(debug=True,port=5200)
