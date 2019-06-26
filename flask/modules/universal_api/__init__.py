from .dispatcher import Dispatcher
from .rest_api import rest
from .universal_api import UniversalApi

class UniversalApiException(Exception):
    pass


dispatcher = Dispatcher()