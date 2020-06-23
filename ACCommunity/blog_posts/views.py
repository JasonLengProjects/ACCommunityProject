# To-do
# 1. DONE! change the redirect of create post view and delete post view to post list view
# 2. add pictures to create post view (need to change db model and form)
# 3. DONE! Add titles to templates
# 4. DONE! add profile image next to each post
# 5. DONE! make usernames in posts clickable
import os
from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import current_user, login_required
from ACCommunity import db
from ACCommunity.models import BlogPost, BlogPostImage
from ACCommunity.blog_posts.forms import BlogPostForm
from ACCommunity.blog_posts.picture_handler import add_post_pic

blog_posts = Blueprint("blog_posts", __name__)


# create post
@blog_posts.route("/create", methods=["GET", "POST"])
@login_required
def create_post():
    form = BlogPostForm()

    if form.validate_on_submit():
        blog_post = BlogPost(title=form.title.data,
                             text=form.text.data,
                             user_id=current_user.id)

        db.session.add(blog_post)
        db.session.commit()

        if form.images.data:
            counter = 0
            for image in form.images.data:
                if image.filename:
                    counter += 1
                    post_id = blog_post.id
                    pic = add_post_pic(image, post_id, counter)
                    new_pic = BlogPostImage(pic, post_id)
                    db.session.add(new_pic)
                    db.session.commit()

        flash("Post created!")
        return redirect(url_for("blog_posts.all_posts"))

    return render_template("create_post.html", form=form, page_title="CREATE POST", show_image=True)


# view single post
@blog_posts.route("/<int:blog_post_id>")
def blog_post(blog_post_id):
    blog_post_found = BlogPost.query.get_or_404(blog_post_id)
    images_found = BlogPostImage.query.filter_by(post_id=blog_post_id)
    print(type(images_found))
    return render_template("blog_post.html", post=blog_post_found, images=images_found, page_title=blog_post_found.title.upper())


# update post
@blog_posts.route("/<int:blog_post_id>/update", methods=["GET", "POST"])
@login_required
def update(blog_post_id):
    blog_post_found = BlogPost.query.get_or_404(blog_post_id)
    if blog_post_found.author != current_user:
        abort(403)

    form = BlogPostForm()

    show_image = False if BlogPostImage.query.filter_by(post_id=blog_post_id).first() else True

    if form.validate_on_submit():

        if form.images.data:
            counter = 0
            for image in form.images.data:
                counter += 1
                post_id = blog_post_found.id
                pic = add_post_pic(image, post_id, counter)
                new_pic = BlogPostImage(pic, post_id)
                db.session.add(new_pic)
                db.session.commit()

        blog_post_found.title = form.title.data
        blog_post_found.text = form.text.data

        db.session.commit()

        flash("Post updated!")
        return redirect(url_for("blog_posts.blog_post", blog_post_id=blog_post_found.id))

    elif request.method == "GET":
        form.title.data = blog_post_found.title
        form.text.data = blog_post_found.text

    return render_template("create_post.html", form=form, show_image=show_image, page_title=blog_post_found.title.upper())


# delete post
@blog_posts.route("/<int:blog_post_id>/delete", methods=["GET", "POST"])
@login_required
def delete_post(blog_post_id):
    blog_post_found = BlogPost.query.get_or_404(blog_post_id)
    if blog_post_found.author != current_user:
        abort(403)

    images_found = BlogPostImage.query.filter_by(post_id=blog_post_id)
    basedir = os.path.abspath(os.getcwd())
    image_dir = os.path.join(basedir, "ACCommunity/static/blog_post_pics")
    for image in images_found:
        os.remove(os.path.join(image_dir, image.post_image))
        db.session.delete(image)
        db.session.commit()

    db.session.delete(blog_post_found)
    db.session.commit()

    flash("Post Deleted!")

    return redirect(url_for("blog_posts.all_posts"))


# view all posts
@blog_posts.route("/all")
def all_posts():
    page = request.args.get("page", 1, type=int)
    all_posts_found = BlogPost.query.order_by(BlogPost.date.desc()).paginate(page=page, per_page=5)
    return render_template("all_posts.html", all_posts=all_posts_found, page_title="ALL POSTS")


