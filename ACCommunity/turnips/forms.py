# To-do
# 1. add error message to html for invalid form inputs
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length


class TurnipPostForm(FlaskForm):
    text = TextAreaField("Text", validators=[DataRequired()])
    turnip_price = IntegerField("Turnip Price",
                                validators=[DataRequired(),
                                            NumberRange(min=0, max=700, message="Invalid Price Entered!")])
    island_code = StringField("Island Code",
                              validators=[DataRequired(),
                                          Length(min=6, max=6, message="Invalid Code Entered!")])
    island_name = StringField("Island Name", validators=[DataRequired()])
    submit = SubmitField("Post")

