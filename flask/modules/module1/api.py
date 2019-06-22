from flask_restful import Resource


class HelloWorldAPI(Resource):
    def get(self):
        return 'Hello world!', 200