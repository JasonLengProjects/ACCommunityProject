from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, MultipleFileField
from wtforms.validators import DataRequired
from ACCommunity.models import BlogPostImage
from flask_wtf.file import FileField, FileAllowed


class BlogPostForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    text = TextAreaField("Text", validators=[DataRequired()])
    images = MultipleFileField("Image(s) Upload", render_kw={"multiple": True})
    # images = FileField("Update Image", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Post")

