from back_end import app, User, db, FuelQuote
import unittest
from flask import url_for
from flask_testing import TestCase


from back_end import app


class TestApp(TestCase):

    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_home(self):
        response = self.client.get(url_for('home'))
        self.assertEqual(response.status_code, 200)
        
    def test_login(self):
        response = self.client.get(url_for('login'))
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get(url_for('register'))
        self.assertEqual(response.status_code, 200)

    def test_user(self):
        response = self.client.get(url_for('user'))
        self.assertEqual(response.status_code, 302)

    def test_logout(self):
        response = self.client.get(url_for('logout'))
        self.assertEqual(response.status_code, 302)
       
    def test_fquote(self):
        response = self.client.get(url_for('fquote'))
        self.assertEqual(response.status_code, 200)
        
    def test_hquote(self):
        response = self.client.get(url_for('hquote'))
        self.assertEqual(response.status_code, 200)

    def test_view(self):
        response = self.client.get(url_for('view'))
        self.assertEqual(response.status_code, 200)
        
    #added NEW TEST CASES FOR MORE COVERAGE EVERYTHING BELOW
    def test_register_post(self):
        response = self.client.post(url_for('register'), data=dict(username="testuser", email="testuser@example.com"), follow_redirects=True)
        self.assertIn(b'Sign Up Successful!', response.data)
        self.assertEqual(response.status_code, 200)

    def test_login_post(self):
        self.client.post(url_for('register'), data=dict(username="testuser", email="testuser@example.com"), follow_redirects=True)
        response = self.client.post(url_for('login'), data=dict(nm="testuser"), follow_redirects=True)
        self.assertIn(b'Login Successful!', response.data)
        self.assertEqual(response.status_code, 200)

    def test_create_fquote(self):
        self.client.post(url_for('register'), data=dict(username="testuser", email="testuser@example.com"), follow_redirects=True)
        self.client.post(url_for('login'), data=dict(nm="testuser"), follow_redirects=True)

        response = self.client.post(url_for('fquote'), data=dict(gallons_requested=1000, delivery_address="123 Test St", delivery_date="2023-05-01"), follow_redirects=True)
        self.assertIn(b'Fuel quote created successfully!', response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_account(self):
        self.client.post(url_for('register'), data=dict(username="testuser", email="testuser@example.com"), follow_redirects=True)
        self.client.post(url_for('login'), data=dict(nm="testuser"), follow_redirects=True)
        response = self.client.post(url_for('delete'), follow_redirects=True)
        self.assertIn(b'Your account has been deleted!', response.data)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
