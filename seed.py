"""Seed file to make sample data for db."""

from models import User, Post, PostTag, Tag, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

User.query.delete()
Post.query.delete()
PostTag.query.delete()
Tag.query.delete()

#sample users
tim = User(first_name="Tim", last_name="Burton")
tessa = User(first_name="Tessa", last_name="Thompson")
liz = User(first_name="Liz", last_name="Inez")
jake = User(first_name="Jake", last_name="Jacob")

db.session.add_all([tim, tessa, liz, jake])
db.session.commit()

#sample posts
post1 = Post(title="First Post", content="This is my first post!", user_id="1")
post2 = Post(title="My Post", content="This is my post!", user_id="2")
post3 = Post(title="Another Post", content="Here's another post!", user_id="3")
post4 = Post(title="Last Post", content="Last post!", user_id="4")

db.session.add_all([post1, post2, post3, post4])
db.session.commit()

#sample tags
tag1 = Tag(name="First")
tag2 = Tag(name="TBT")
tag3 = Tag(name="Food")
tag4 = Tag(name="Blogly")

db.session.add_all([tag1, tag2, tag3, tag4])
db.session.commit()

#sample posts_tags
pt1 = PostTag(post_id=1, tag_id=1)
pt2 = PostTag(post_id=2, tag_id=2)
pt3 = PostTag(post_id=3, tag_id=3)
pt4 = PostTag(post_id=4, tag_id=4)

db.session.add_all([pt1, pt2, pt3, pt4])
db.session.commit()
