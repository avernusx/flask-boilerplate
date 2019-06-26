from flask import Blueprint
from modules.universal_api import rest, UniversalApi
from .models import HelloWorldModel
from .schemas import HelloWorldSchema

blueprint = Blueprint('radio', __name__, url_prefix='/api/radio/')

@rest(blueprint, 'hello')
class HelloWorldApi(UniversalApi):
    model = HelloWorldModel
    schema = HelloWorldSchema