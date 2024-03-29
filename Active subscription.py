from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MySQL Configuration
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'BloggingPlatform'
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
