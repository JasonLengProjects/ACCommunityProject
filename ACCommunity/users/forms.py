# To-do:
# 1. add validation error in html template (check lecture 110 Q&A)
# 2. add validation error for villager forms
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed

from flask_login import current_user
from ACCommunity.models import User


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class RegistrationForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username (Name on your posts)", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired(),
                                                     EqualTo("password_confirm", message="Passwords Must Math")])
    password_confirm = PasswordField("Confirm Password", validators=[DataRequired()])
    checkbox = BooleanField("I'm not a robot", validators=[InputRequired()])
    submit = SubmitField("Register!")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("Your email has been registered already!")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Your username has already been taken!")


class UpdateUserForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    username = StringField("Username", validators=[DataRequired()])
    picture = FileField("Update Profile Image", validators=[FileAllowed(["jpg", "jpeg", "png"])])
    submit = SubmitField("Update")

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is not None and User.query.filter_by(
                email=field.data).first().email == current_user.email:
            return
        elif User.query.filter_by(email=field.data).first():
            raise ValidationError("This email has been registered already!")

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first() is not None and User.query.filter_by(
                username=field.data).first().username == current_user.username:
            return
        elif User.query.filter_by(username=field.data).first():
            raise ValidationError("This username has already been taken!")
