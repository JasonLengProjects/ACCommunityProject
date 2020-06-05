# To-do
# DONE! 1. add functionality to delete villagers
# DONE! 2. add villager list view
# 2.1. add filter functionality to list view
# DONE! 3. add bootstrap style to villager info view

from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_required, current_user
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
        return redirect(url_for("villagers.villager_info", villager_name=villager.name))

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
        if villager_name != form.name.data and Villager.query.filter_by(name=form.name.data):
            flash("Villager with same name added already!", "error")
            return render_template("edit_villager.html", villager=villager, form=form)

        if form.picture.data:
            pic = add_profile_pic(form.picture.data, villager.name)
            villager.image = pic

        villager.name = form.name.data
        villager.personality = form.personality.data
        villager.species = form.species.data
        villager.birthday = form.birthday.data

        db.session.commit()

        flash("Villager information updated!")
        return redirect(url_for("villagers.villager_info", villager_name=villager.name))

    elif request.method == "GET":
        form.name.data = villager.name
        form.personality.data = villager.personality
        form.species.data = villager.species
        form.birthday.data = villager.birthday

    return render_template("edit_villager.html", villager=villager, form=form)


# delete villager
@villagers.route("/<villager_name>/delete", methods=["GET", "POST"])
@login_required
def delete_villager(villager_name):
    villager_found = Villager.query.filter_by(name=villager_name).first_or_404()
    if current_user.username != "One_edit":
        abort(403)

    db.session.delete(villager_found)
    db.session.commit()

    flash("Villager Deleted!")

    return redirect(url_for("villagers.all_villagers"))


# view all villagers
@villagers.route("/all")
def all_villagers():
    page = request.args.get("page", 1, type=int)
    all_villagers_found = Villager.query.order_by(Villager.name).paginate(page=page, per_page=5)
    return render_template("all_villagers.html", all_villagers=all_villagers_found)







