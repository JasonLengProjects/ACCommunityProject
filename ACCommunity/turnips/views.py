from flask import render_template, url_for, flash, request, redirect, Blueprint
from flask_login import current_user, login_required
from ACCommunity import db
from ACCommunity.models import TurnipPost
from ACCommunity.turnips.forms import TurnipPostForm

turnip_posts = Blueprint("turnip_posts", __name__)


# create turnip post
@turnip_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = TurnipPostForm()

    if form.validate_on_submit():

        turnip_post = TurnipPost(text=form.text.data,
                                 turnip_price=form.turnip_price.data,
                                 island_code=form.island_code.data,
                                 island_name=form.island_name.data,
                                 user_id=current_user.id)

        db.session.add(turnip_post)
        db.session.commit()

        flash("Turnip Post Created!")
        return redirect(url_for("turnip_posts.all_posts"))

    return render_template("create_turnip_post.html", form=form, page_title="CREATE POST")


# view single post
@turnip_posts.route("/<int:turnip_post_id>")
def turnip_post(turnip_post_id):
    turnip_post_found = TurnipPost.query.get_or_404(turnip_post_id)
    return render_template("turnip_post.html", post=turnip_post_found, page_title="ISLAND-"+turnip_post_found.island_name)


# update post
@turnip_posts.route("/<int:turnip_post_id>/update", methods=["GET", "POST"])
@login_required
def update(turnip_post_id):
    turnip_post_found = TurnipPost.query.get_or_404(turnip_post_id)
    if turnip_post_found.host != current_user:
        abort(403)

    form = TurnipPostForm()

    if form.validate_on_submit():
        turnip_post_found.text = form.text.data
        turnip_post_found.turnip_price = form.turnip_price.data
        turnip_post_found.island_code = form.island_code.data
        turnip_post_found.island_name = form.island_name.data

        db.session.commit()

        flash("Turnip Post Updated!")
        return redirect(url_for("turnip_posts.turnip_post", turnip_post_id=turnip_post_found.id))

    elif request.method == "GET":
        form.text.data = turnip_post_found.text
        form.turnip_price.data = turnip_post_found.turnip_price
        form.island_code.data = turnip_post_found.island_code
        form.island_name.data = turnip_post_found.island_name

    return render_template("create_turnip_post.html", form=form, page_title="UPDATE")


# delete post
@turnip_posts.route("/<int:turnip_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(turnip_post_id):
    turnip_post_found = TurnipPost.query.get_or_404(turnip_post_id)
    if turnip_post_found.host != current_user:
        abort(403)

    db.session.delete(turnip_post_found)
    db.session.commit()

    flash("Post Deleted!")

    return redirect(url_for("turnip_posts.all_posts"))


# view all posts
@turnip_posts.route("/all")
def all_posts():
    page = request.args.get("page", 1, type=int)
    all_posts_found = TurnipPost.query.order_by(TurnipPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("all_turnip_posts.html", all_posts=all_posts_found, page_title="ALL POSTS")


