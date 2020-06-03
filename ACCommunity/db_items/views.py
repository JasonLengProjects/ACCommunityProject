# To-do
# 1. add functionality to delete villagers
# 2. add villager list view
# 2.1. add filter functionality to list view
# 3. add bootstrap style to villager info view

from flask import render_template, url_for, flash, redirect, request, Blueprint
from ACCommunity import db
from ACCommunity.models import Villager
from ACCommunity.db_items.forms import AddVillagerForm, EditVillagerForm
from ACCommunity.db_items.picture_handler import add_profile_pic

villagers = Blueprint("villagers", __name__)


# add new villager
@villagers.route("/add", methods=["GET", "POST"])
def add_villager():
    form = AddVillagerForm()

    if form.validate_on_submit():
        villager = Villager(name=form.name.data,
                            personality=form.personality.data,
                            species=form.species.data,
                            birthday=form.birthday.data)

        db.session.add(villager)
        db.session.commit()

        flash("Villager added!")
        return redirect(url_for("core.index"))

    return render_template("add_villager.html", form=form)


# single villager view
@villagers.route("/<villager_name>")
def villager_info(villager_name):
    villager = Villager.query.filter_by(name=villager_name).first_or_404()

    return render_template("villager_info.html", villager=villager)


# edit villager
@villagers.route("/<villager_name>/edit", methods=["GET", "POST"])
def edit_villager(villager_name):
    form = EditVillagerForm()
    villager = Villager.query.filter_by(name=villager_name).first_or_404()

    if form.validate_on_submit():
        if form.picture.data:
            pic = add_profile_pic(form.picture.data, villager.name)
            villager.image = pic

        villager.name = form.name.data
        villager.personality = form.personality.data
        villager.species = form.species.data
        villager.birthday = form.birthday.data
        db.session.commit()

        flash("Villager information updated!")
        return redirect(url_for("villagers.villager_info"))

    elif request.method == "GET":
        form.name.data = villager.name
        form.personality.data = villager.personality
        form.species.data = villager.species
        form.birthday.data = villager.birthday

    return render_template("edit_villager.html", villager=villager, form=form)







