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
        


if __name__ == '__main__':
    unittest.main()
