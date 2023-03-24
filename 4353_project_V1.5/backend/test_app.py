import unittest
from flask import url_for
from flask_testing import TestCase

from app import app


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
        


if __name__ == '__main__':
    unittest.main()
