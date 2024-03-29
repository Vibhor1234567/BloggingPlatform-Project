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
