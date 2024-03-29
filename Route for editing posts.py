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
