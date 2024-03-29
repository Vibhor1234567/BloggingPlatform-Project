from flask import Flask, request, session, redirect, url_for, render_template
import mysql.connector
from passlib.hash import sha256_crypt
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators, TextAreaField
from datetime import datetime, timedelta


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
    
if __name__ == '__main__':
    app.run(debug=True)



# Creating forms for user login,logout and account creation.
# Login Form('login.html'):
## <!DOCTYPE html>
## <html lang="en">
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="POST" action="{{ url_for('login') }}">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p>Don't have an account? <a href="{{ url_for('register') }}">Register here</a>.</p>
</body>
</html>

# Registration Form('registration.html'):
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Register</title>
</head>
<body>
    <h2>Register</h2>
    <form method="POST" action="{{ url_for('register') }}">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" required><br><br>
        <label for="password">Password:</label>
        <input type="password" id="password" name="password" required><br><br>
        <label for="email">Email:</label>
        <input type="email" id="email" name="email" required><br><br>
        <button type="submit">Register</button>
    </form>
    <p>Already have an account? <a href="{{ url_for('login') }}">Login here</a>.</p>
</body>
</html>



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Handle login form submission
        # ...
    else:
        return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Handle registration form submission
        # ...
    else:
        return render_template('register.html')




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

        # Retrieve user from database
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and sha256_crypt.verify(password, user[2]):  # Verify hashed password
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password!"

    return render_template('login.html', form=form)

# User Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard (Protected Route)
@app.route('/dashboard')
def dashboard():
    if 'logged_in' in session:
        return f"Welcome {session['username']}! You are logged in."
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)



# Define subscription plans with expiration dates
subscription_plans = {
    'basic': {
        'post_limit': 5,
        'expiration_period': timedelta(days=10)
    },
    'premium': {
        'post_limit': 10,
        'expiration_period': timedelta(days=10)
    }
}




# Function to check if a user has an active subscription
def has_active_subscription(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to check if the user has an active subscription
    cursor.execute("""
    SELECT * FROM user_subscribed_subscription
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))
    active_subscription = cursor.fetchone()

    conn.close()

    return active_subscription is not None

# Function to check if a user has reached their post limit for the subscription
def has_reached_post_limit(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to count the number of posts by the user
    cursor.execute("SELECT COUNT(*) FROM posts WHERE author_id = %s", (user_id,))
    post_count = cursor.fetchone()[0]

    conn.close()

    # Get the user's subscription plan
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT subscription_id FROM user_subscribed_subscription
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))
    subscription_id = cursor.fetchone()

    if subscription_id:
        cursor.execute("""
        SELECT post_limit FROM subscriptions
        WHERE subscription_id = %s
        """, (subscription_id,))
        post_limit = cursor.fetchone()[0]

        return post_count >= post_limit
    else:
        return True  # No active subscription, restrict posting

    conn.close()

# Function to purchase a new subscription plan
def purchase_subscription(user_id, plan_name):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Get the subscription details based on the plan name
    cursor.execute("SELECT * FROM subscriptions WHERE plan_name = %s", (plan_name,))
    subscription_details = cursor.fetchone()
    if subscription_details is None:
        conn.close()
        return "Invalid subscription plan."

    subscription_id = subscription_details[0]
    post_limit = subscription_details[2]
    expiration_period = subscription_details[3]

    # Mark previous subscriptions as expired
    cursor.execute("""
    UPDATE user_subscribed_subscription
    SET end_date = NOW()
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))

    # Insert new subscription into user_subscribed_subscription table
    start_date = datetime.now()
    end_date = start_date + expiration_period
    cursor.execute("""
    INSERT INTO user_subscribed_subscription (user_id, subscription_id, start_date, end_date)
    VALUES (%s, %s, %s, %s)
    """, (user_id, subscription_id, start_date, end_date))

    conn.commit()
    conn.close()

    return "Subscription purchased successfully!"

# Example usage:
user_id = 1  # Assuming the user ID
plan_name = "premium"  # Plan name to purchase

print(purchase_subscription(user_id, plan_name))




# Function to retrieve paginated blog posts
def get_paginated_posts(page_number, posts_per_page):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Calculate offset for pagination
    offset = (page_number - 1) * posts_per_page

    # Query to fetch paginated blog posts
    cursor.execute("""
    SELECT p.title, p.description, p.publication_date, u.username
    FROM posts p
    INNER JOIN users u ON p.author_id = u.user_id
    ORDER BY p.publication_date DESC
    LIMIT %s OFFSET %s
    """, (posts_per_page, offset))

    posts = cursor.fetchall()

    conn.close()

    return posts

# Homepage route
@app.route('/')
def homepage():
    # Get page number from query string or default to page 1
    page_number = int(request.args.get('page', 1))

    # Number of posts per page
    posts_per_page = 10

    # Retrieve paginated blog posts
    posts = get_paginated_posts(page_number, posts_per_page)

    return render_template('homepage.html', posts=posts)

if __name__ == '__main__':
    app.run(debug=True)



# Define BlogPostForm class
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[validators.InputRequired()])
    description = TextAreaField('Description', validators=[validators.InputRequired()])
    # You can add more fields as needed (e.g., author, image upload)



# HTML Template (HTML/Jinja2):
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Create New Blog Post</title>
</head>
<body>
    <h1>Create New Blog Post</h1>
    <form method="POST" enctype="multipart/form-data">
        {{ form.hidden_tag() }}
        <div>
            {{ form.title.label }}
            {{ form.title(size=50) }}
            {% for error in form.title.errors %}
                <p style="color: red;">{{ error }}</p>
            {% endfor %}
        </div>
        <div>
            {{ form.description.label }}
            {{ form.description(cols=50, rows=10) }}
            {% for error in form.description.errors %}
                <p style="color: red;">{{ error }}</p>
            {% endfor %}
        </div>
        <!-- Add more form fields here as needed -->
        <div>
            <button type="submit">Submit</button>
        </div>
    </form>
</body>
</html>




# Function to check if a user has an active subscription
def has_active_subscription(user_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to check if the user has an active subscription
    cursor.execute("""
    SELECT * FROM user_subscribed_subscription
    WHERE user_id = %s AND end_date > NOW()
    """, (user_id,))
    active_subscription = cursor.fetchone()

    conn.close()

    return active_subscription is not None

# Function to save blog post for users with active subscriptions
def save_blog_post(title, description, author_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    if has_active_subscription(author_id):
        # Insert the blog post into the database
        cursor.execute("INSERT INTO posts (title, description, author_id, publication_date) VALUES (%s, %s, %s, %s)", (title, description, author_id, datetime.now()))
        conn.commit()
        conn.close()
        return True
    else:
        conn.close()
        return False

# Route to handle blog post creation
@app.route('/create_post', methods=['GET', 'POST'])
def create_post():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        author_id = 1  # Assuming the user ID. You can fetch it from the session or wherever it's stored.

        # Save the blog post only if the user has an active subscription
        if save_blog_post(title, description, author_id):
            flash('Blog post saved successfully!')
            return redirect(url_for('homepage'))
        else:
            flash('You need an active subscription to save blog posts.')
            return redirect(url_for('create_post'))

    return render_template('create_post.html')

if __name__ == '__main__':
    app.run(debug=True)


# Route to handle editing of blog posts
@app.route('/edit_post/<int:post_id>', methods=['GET', 'POST'])
def edit_post(post_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch the post details from the database
    cursor.execute("SELECT * FROM posts WHERE post_id = %s", (post_id,))
    post = cursor.fetchone()
    conn.close()

    if post:
        # Check if the logged-in user is the author of the post (you may need to implement this logic)
        # Assuming author_id is stored in session or somewhere accessible
        author_id = 1  # Replace with the actual author_id
        if post[3] == author_id:
            if request.method == 'POST':
                # Update the post with the edited content
                title = request.form['title']
                description = request.form['description']

                conn = mysql.connector.connect(**db_config)
                cursor = conn.cursor()

                cursor.execute("UPDATE posts SET title = %s, description = %s WHERE post_id = %s", (title, description, post_id))
                conn.commit()
                conn.close()

                flash('Post updated successfully!')
                return redirect(url_for('homepage'))
            else:
                return render_template('edit_post.html', post=post)
        else:
            flash('You are not authorized to edit this post.')
            return redirect(url_for('homepage'))
    else:
        flash('Post not found.')
        return redirect(url_for('homepage'))
    

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Edit Post</title>
</head>
<body>
    <h1>Edit Post</h1>
    <form method="POST">
        {{ form.hidden_tag() }}
        <div>
            <label for="title">Title:</label>
            <input type="text" id="title" name="title" value="{{ post[1] }}" required>
        </div>
        <div>
            <label for="description">Description:</label>
            <textarea id="description" name="description" rows="4" required>{{ post[2] }}</textarea>
        </div>
        <button type="submit">Update Post</button>
    </form>
</body>
</html>




# Route to display detailed blog post information
@app.route('/post/<int:post_id>')
def post_details(post_id):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Fetch the details of the post from the database
    cursor.execute("""
    SELECT p.title, p.description, p.publication_date, u.username
    FROM posts p
    INNER JOIN users u ON p.author_id = u.user_id
    WHERE p.post_id = %s
    """, (post_id,))
    post = cursor.fetchone()

    conn.close()

    if post:
        return render_template('post_details.html', post=post)
    else:
        flash('Post not found.')
        return redirect(url_for('homepage'))




<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ post[0] }}</title>
</head>
<body>
    <h1>{{ post[0] }}</h1> <!-- Post title -->
    <p>Author: {{ post[3] }}</p> <!-- Author username -->
    <p>Publication Date: {{ post[2] }}</p> <!-- Publication date -->
    <div>
        {{ post[1] }} <!-- Post content -->
    </div>
</body>
</html>






# Function to fetch filtered blog posts based on date range
def get_filtered_posts(start_date, end_date):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to fetch blog posts within the specified date range
    cursor.execute("""
    SELECT p.title, p.description, p.publication_date, u.username
    FROM posts p
    INNER JOIN users u ON p.author_id = u.user_id
    WHERE p.publication_date BETWEEN %s AND %s
    ORDER BY p.publication_date DESC
    """, (start_date, end_date))

    posts = cursor.fetchall()

    conn.close()

    return posts

# Homepage route with date filter
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Get start date and end date from form submission
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        # Fetch filtered blog posts
        posts = get_filtered_posts(start_date, end_date)

        return render_template('homepage.html', posts=posts)

    # Default behavior: render homepage without filtering
    return render_template('homepage.html', posts=None)

if __name__ == '__main__':
    app.run(debug=True)




# Function to fetch posts matching search query
def search_posts(query):
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor()

    # Query to fetch posts matching the search query in title, description, or author username
    cursor.execute("""
    SELECT p.title, p.description, p.publication_date, u.username
    FROM posts p
    INNER JOIN users u ON p.author_id = u.user_id
    WHERE p.title LIKE %s OR p.description LIKE %s OR u.username LIKE %s
    ORDER BY p.publication_date DESC
    """, (f'%{query}%', f'%{query}%', f'%{query}%'))

    posts = cursor.fetchall()

    conn.close()

    return posts

# Homepage route with search functionality
@app.route('/', methods=['GET', 'POST'])
def homepage():
    if request.method == 'POST':
        # Get search query from form submission
        search_query = request.form['search_query']

        # Fetch posts matching the search query
        posts = search_posts(search_query)

        return render_template('homepage.html', posts=posts, search_query=search_query)

    # Default behavior: render homepage without search results
    return render_template('homepage.html', posts=None, search_query=None)

if __name__ == '__main__':
    app.run(debug=True)