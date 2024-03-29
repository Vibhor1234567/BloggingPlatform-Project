from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

# MySQL Configuration
db_config = {
    'host': 'your_host',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'BloggingPlatform'
}

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
