from flask import Blueprint
from flask_restful import Api
from .api import HelloWorldAPI, TestInstanceAPI, TestListAPI
from .tests import MyTest

blueprint = Blueprint('api', __name__, url_prefix='/api/module1/')
api = Api(blueprint)

api.add_resource(HelloWorldAPI, 'hello_world')
api.add_resource(TestListAPI, 'tests')
api.add_resource(TestInstanceAPI, 'test')
api.add_resource(TestInstanceAPI, 'test/<string:slug>', endpoint='test.instance')