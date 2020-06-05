import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecret"

# Database setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
Migrate(app, db)

# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "users.login"


from ACCommunity.core.views import core
from ACCommunity.users.views import users
from ACCommunity.db_items.views import villagers
from ACCommunity.blog_posts.views import blog_posts
from ACCommunity.turnips.views import turnip_posts
from ACCommunity.error_pages.handlers import error_pages
app.register_blueprint(core)
app.register_blueprint(users, url_prefix="/users")
app.register_blueprint(villagers, url_prefix="/villagers")
app.register_blueprint(blog_posts, url_prefix="/blog_posts")
app.register_blueprint(turnip_posts, url_prefix="/turnip_posts")
app.register_blueprint(error_pages)



