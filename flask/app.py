import os
from importlib import import_module
from flask import Flask, request


app = Flask(__name__, static_url_path="")

# подключение модулей
skip = ['__pycache__']

for folder in os.listdir('./modules'):
    if os.path.isdir(os.path.join('./modules', folder)) and folder not in skip:
        module = import_module('modules.' + folder)
        app.register_blueprint(module.blueprint)