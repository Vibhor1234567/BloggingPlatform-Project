from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '12345',
    'database': 'BloggingPlatform'
}

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
