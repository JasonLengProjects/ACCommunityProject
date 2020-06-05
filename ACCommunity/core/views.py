# for home view and info  view
from flask import render_template, request, Blueprint

core = Blueprint("core", __name__)


@core.route("/")
def index():
    return render_template("index.html", page_title="HOME")


@core.route("/about")
def about():
    return render_template("about.html", page_title="ABOUT")

