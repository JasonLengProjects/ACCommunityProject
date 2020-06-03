# To-do
# 1. add bootstrap styles to register.html
# 2. add profile image to posts
# 3. implement queue function for showing island codes
# 4. create link for showing turnip posts
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from ACCommunity import db
from ACCommunity.models import User, BlogPost, TurnipPost
from ACCommunity.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from ACCommunity.users.picture_handler import add_profile_pic

users = Blueprint("users", __name__)


# register
@users.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(email=form.email.data,
                    username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()

        flash("Thanks for your registration!")
        return redirect(url_for("users.login"))

    return render_template("register.html", form=form)


# login
@users.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user.check_password(form.password.data) and user is not None:
            login_user(user)
            flash("Log in successfully!")

            next_page = request.args.get("next")

            if next_page is None or not next_page[0] == "/":
                next_page = url_for("core.index")

            return redirect(next_page)

    return render_template("login.html", form=form)


# logout
@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("core.index"))


# account
@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateUserForm()
    if form.validate_on_submit():
        if form.picture.data:
            username = current_user.username
            pic = add_profile_pic(form.picture.data, username)
            current_user.profile_image = pic

        current_user.username = form.username.data
        current_user.email = form.email.data

        db.session.commit()

        flash("User information updated!")
        return redirect(url_for("users.account"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    profile_image = url_for('static', filename="profile_pics"+current_user.profile_image)

    return render_template("account.html", profile_image=profile_image, form=form)


# list of blog posts
@users.route("/blog/<username>")
def user_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    blog_posts = BlogPost.query.filter_by(author=user).order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("user_blog_posts.html", blog_posts=blog_posts, user=user)


# list of turnip posts
@users.route("/turnip/<username>")
def user_turnip_posts(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    turnip_posts = TurnipPost.query.filter_by(host=user).order_by(TurnipPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("user_turnip_posts.html", turnip_posts=turnip_posts, user=user)

