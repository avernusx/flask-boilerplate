from flask import Blueprint
from flask_restful import Api
from .api import HelloWorldAPI

blueprint = Blueprint('api', __name__, url_prefix='/api/module1/')
api = Api(blueprint)

api.add_resource(HelloWorldAPI, 'hello_world')