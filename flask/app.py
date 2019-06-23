import os
from importlib import import_module
from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic


def create_app():
    app = Flask(__name__, static_url_path="")

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://docker:docker@postgresql:5432/site'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['ALEMBIC'] = {
        'script_location': 'migrations',
        'version_locations': []
    }

    database = SQLAlchemy(app)

    # подключение модулей
    skip = ['__pycache__']

    for folder in os.listdir('./modules'):
        if os.path.isdir(os.path.join('./modules', folder)) and folder not in skip:
            module = import_module('modules.' + folder)
            if hasattr(module, 'blueprint'):
                app.register_blueprint(module.blueprint)
            app.config['ALEMBIC']['version_locations'] = (
                    folder, 'modules/{}/migrations'.format(folder)
            )

    return app

app = create_app()

alembic = Alembic()
alembic.init_app(app)