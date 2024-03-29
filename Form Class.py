from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, validators

# Define BlogPostForm class
class BlogPostForm(FlaskForm):
    title = StringField('Title', validators=[validators.InputRequired()])
    description = TextAreaField('Description', validators=[validators.InputRequired()])
    # You can add more fields as needed (e.g., author, image upload)
