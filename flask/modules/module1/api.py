from flask_restful import Resource
from modules.universal_api import UniversalListAPI, UniversalInstanceAPI
from .models import TestClass
from .schemas import TestSchema


class HelloWorldAPI(Resource):
    def get(self):
        return 'Hello world!', 200


class TestInstanceAPI(UniversalInstanceAPI):
    model = TestClass
    schema = TestSchema

class TestListAPI(UniversalListAPI):
    model = TestClass
    schema = TestSchema