from distutils.command.build_scripts import first_line_re
from unittest import TestCase

from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
   """Tests for model for Users"""

   def setUp(self):
      """Clean up any existing users"""
      User.query.delete()

   def tearDown(self):
      """Clean up any fouled transaction"""
      db.session.rollback()

   def test_name(self):
      user = User(first_name="Tom", last_name="Thompson")
      db.session.add(user)
      db.session.commit()

      self.assertEqual(user.first_name, "Tom")
      self.assertEqual(user.last_name, "Thompson")
      self.assertEqual(user.full_name, "Tom Thompson")