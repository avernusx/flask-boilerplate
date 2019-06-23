from flask_testing import TestCase
from app import create_app

class MyTest(TestCase):
    def create_app(self):
        return create_app()

    def test_something(self):
        pass