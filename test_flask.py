from unittest import TestCase

from sqlalchemy import true
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db_test'
app.config['SQLALCHEMY_ECHO'] = False

app.config['TESTING'] = True

app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserTestCase(TestCase):
   """Test user info display"""

   def setUp(self):
      """Add sample User"""

      User.query.delete()

      user = User(first_name="Tom", last_name="Thompson")
      db.session.add(user)
      db.session.commit()

      self.user_id = user.id

   def tearDown(self):
      """Clean up any fouled transaction"""
      db.session.rollback()

   def test_list_users(self):
      """Check if user is added to list of users"""
      with app.test_client() as client:
         resp = client.get('/users')
         html = resp.get_data(as_text=True)

         self.assertEqual(resp.status_code, 200)
         self.assertIn("Tom Thompson", html)

   def test_show_user(self):
      """Check if user is clicked, redirect to user's info page"""
      with app.test_client() as client:
         resp = client.get(f"/users/{self.user_id}")
         html = resp.get_data(as_text=True)

         self.assertEqual(resp.status_code, 200)
         self.assertIn('<h1>Tom Thompson</h1>', html)
      
      def test_new_user(self):
         """After new user input, check redirect to users list"""
         with app.test_client() as client:
            d = {'first_name': 'Test', 'last_name': 'Name'}
            resp = client.post('/users/new', data = d)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertEqual(resp.location, '/users')