# To-do
# 1. make some fields in the edit form not required
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms import ValidationError
from flask_wtf.file import FileField, FileAllowed
from ACCommunity.models import Villager


class AddVillagerForm(FlaskForm):
    name = StringField("Villager Name", validators=[DataRequired()])
    personality = StringField("Personality", validators=[DataRequired()])
    species = StringField("Species", validators=[DataRequired()])
    birthday = StringField("Birthday (Month)", validators=[DataRequired()])
    picture = FileField("Add Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit = SubmitField("Add Villager")

    def validate_name(self, field):
        if Villager.query.filter_by(name=field.data).first():
            raise ValidationError("Villager with same name added already!")


class EditVillagerForm(FlaskForm):
    name = StringField("Villager Name", validators=[DataRequired()])
    personality = StringField("Personality", validators=[DataRequired()])
    species = StringField("Species", validators=[DataRequired()])
    birthday = StringField("Birthday (Month)", validators=[DataRequired()])
    picture = FileField("Change Picture", validators=[FileAllowed(["jpg", "jpeg", "png"])])

    submit = SubmitField("Update Villager")

    def validate_name(self, field):
        if Villager.query.filter_by(name=field.data).first():
            raise ValidationError("Villager with same name added already!")



