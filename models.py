"""Models for Blogly."""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

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

def connect_db(app):
   db.app = app
   db.init_app(app)