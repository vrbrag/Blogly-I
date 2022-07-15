"""Models for Blogly."""
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


   @property
   def full_name(self):
      return f"{self.first_name} {self.last_name}"


class Post(db.Model):
   """Posts"""

   __tablename__="posts"

   id = db.Column(db.Integer, primary_key=True, autoincrement=True)
   title = db.Column(db.Text, nullable=False)
   content = db.Column(db.Text, nullable=False)
   created_at = db.Column(db.Date, nullable=False)
   user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

def connect_db(app):
   db.app = app
   db.init_app(app)