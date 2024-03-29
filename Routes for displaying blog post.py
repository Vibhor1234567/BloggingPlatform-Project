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
