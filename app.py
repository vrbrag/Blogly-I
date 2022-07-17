"""Blogly application."""

# from pydoc import render_doc
from wsgiref.handlers import read_environ
from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__,template_folder='templates')
app.debug = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.route('/')
def root():
   """Posts feed"""

   posts = Post.query.order_by(Post.created_at.desc()).limit(8).all()
   return render_template('homepage.html', posts=posts)

###########################################
# Users
###########################################
@app.route('/users')
def show_users():
   """Display list of users and link them"""

   users = User.query.order_by(User.last_name, User.first_name).all()
   return render_template('index.html', users=users)

@app.route('/users/new', methods=["GET"])
def new_user_form():
   """New User Form"""

   return render_template('usernew.html')

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

###########################################
# Posts
###########################################
@app.route('/users/<int:user_id>/posts/new')
def posts_form(user_id):
   """Form to create a new post for this user id"""

   user = User.query.get_or_404(user_id)
   return render_template('postnew.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def new_post(user_id):
   """Handle new post"""

   user = User.query.get_or_404(user_id)
   new_post = Post(
               title = request.form['title'], 
               content = request.form['content'],
               user=user)
   
   db.session.add(new_post)
   db.session.commit()
   flash(f"Post '{ new_post.title }' added!")

   return redirect(f"/users/{user_id}")

@app.route('/posts/<int:post_id>')
def show_posts(post_id):
   """Show info of a specific post"""

   post = Post.query.get_or_404(post_id)
   return render_template('postshow.html', post=post)

@app.route('/posts/<int:post_id>/edit')
def edit_post(post_id):
   """Form to edit specific post"""

   post = Post.query.get_or_404(post_id)
   return render_template('postedit.html', post=post) 

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def update_post(post_id):
   """Handle edited specific post"""

   post = Post.query.get_or_404(post_id)
   post.title = request.form['title']
   post.content = request.form['content']

   db.session.add(post)
   db.session.commit()
   flash(f"Post '{ post.title}' has been edited.")

   return redirect(f"/users/{post.user_id}")

@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
   """Delete specific post"""

   post = Post.query.get_or_404(post_id)
   db.session.delete(post)
   db.session.commit()
   flash(f"Post '{post.title}' has been deleted.")

   return redirect(f"/users/{post.user_id}")