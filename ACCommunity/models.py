# To-do:
# 1. make post text nullable
# 2. add image for turnip posts
# 3. make name villager's primary key
# 4. add admit permission to User to add, edit, delete villagers
# 5. upload picture at the time a villager is created

from ACCommunity import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    profile_image = db.Column(db.String(128), nullable=False, default="default_profile.jpg")
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))

    blog_posts = db.relationship("BlogPost", backref="author", lazy=True)
    turnip_posts = db.relationship("TurnipPost", backref="host", lazy=True)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"Username: {self.username}"


class BlogPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    title = db.Column(db.String(140), nullable=False)
    text = db.Column(db.Text, nullable=False)

    def __init__(self, title, text, user_id):
        self.title = title
        self.text = text
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date} --- {self.title}"


class TurnipPost(db.Model):
    users = db.relationship(User)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)  # table name here
    date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    turnip_price = db.Column(db.Integer, nullable=False)
    text = db.Column(db.Text, nullable=False)
    island_code = db.Column(db.String(64), nullable=False)
    island_name = db.Column(db.String(64), nullable=False)

    def __init__(self, text, turnip_price, island_code, island_name, user_id):
        self.text = text
        self.turnip_price = turnip_price
        self.island_code = island_code
        self.island_name = island_name
        self.user_id = user_id

    def __repr__(self):
        return f"Post ID: {self.id} -- Date: {self.date}"


class Villager(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    personality = db.Column(db.String(64), nullable=False, default="No Personality")
    species = db.Column(db.String(64), nullable=False, default="No Species")
    birthday = db.Column(db.String(64), nullable=False, default="January")
    image = db.Column(db.String(64), nullable=False, default="default_profile.jpg")

    def __init__(self, name, personality, species, birthday):
        self.name = name
        self.personality = personality
        self.species = species
        self.birthday = birthday

    def __repr__(self):
        return f"Name: {self.name} - Personality: {self.personality} - Species: {self.species} - Month: {self.birthday}"



