"""Blogly application."""

# from pydoc import render_doc
from wsgiref.handlers import read_environ
from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__,template_folder='templates')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
   return redirect('/users')

@app.route('/users')
def show_users():
   """Display list of users and link them"""

   users = User.query.order_by(User.last_name, User.first_name).all()
   return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
   """New User Form"""

   return render_template('newuser.html')

@app.route('/users/new', methods=["POST"])
def new_user():
   """Submit new user"""
   new_user = User(
      first_name = request.form['first_name'],
      last_name = request.form['last_name'],
      image_url = request.form['image_url'] or None
   )
   
   db.session.add(new_user)
   db.session.commit()

   return redirect('/users')

@app.route('/users/<int:user_id>')
def show_user(user_id):
   """Show page of user info"""

   user = User.query.get_or_404(user_id)
   return render_template('userinfo.html', user=user)

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
   """Edit user form"""

   user = User.query.get_or_404(user_id)
   return render_template('useredit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def update_user(user_id):
   """Update user info/handle form submission"""

   user = User.query.get_or_404(user_id)
   user.first_name = request.form['first_name']
   user.last_name = request.form['last_name']
   user.image_url = request.form['image_url']

   db.session.add(user)
   db.session.commit()

   return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
   """Delete user info"""

   user = User.query.get_or_404(user_id)

   db.session.delete(user)
   db.session.commit()

   return redirect('/users')

