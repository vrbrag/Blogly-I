"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"



class User(db.Model):
   """Users"""

   __tablename__ = "users"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   first_name = db.Column(db.Text, nullable=False)
   last_name = db.Column(db.Text, nullable=False)
   image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

   posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

   @property
   def full_name(self):
      return f"{self.first_name} {self.last_name}"


class Post(db.Model):
   """Posts"""

   __tablename__="posts"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.Text, nullable=False)
   content = db.Column(db.Text, nullable=False)
   created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

   posttags = db.relationship('PostTag', cascade="all, delete", backref='posts')

   @property
   def friendly_date(self):
      return self.created_at.strftime("%a %b %-d %Y, %-I:%M %p")

   def __repr__(self):
      return f"<User {self.user_id} posted '{self.title}' on {self.friendly_date}>"

class PostTag(db.Model):
   """Tags on a post"""

   __tablename__="posts_tags"

   post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
   tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)


class Tag(db.Model):
   """Tags that can be added to a post"""

   __tablename__="tags"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   name = db.Column(db.Text, nullable=False, unique=True)

   posts = db.relationship('Post', secondary="posts_tags", cascade="all, delete", backref='tags')

   def __repr__(self):
      return f"<This user has tagged '{self.name}'>"


def connect_db(app):
   db.app = app
   db.init_app(app)