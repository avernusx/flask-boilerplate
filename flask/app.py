import os
from importlib import find_loader, import_module
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
            # importing api
            api_path = os.path.join('./modules', folder, 'api')
            api_module = 'modules.' + folder + '.api'
            api = None
            if os.path.isdir(api_path):
                if find_loader(api_module):
                    api = import_module(api_module)
            elif os.path.isfile(api_path + '.py'):
                api = import_module(api_module)
            if api is not None and hasattr(api, 'blueprint'):
                app.register_blueprint(api.blueprint)
            # importing migrations    
            app.config['ALEMBIC']['version_locations'] = (
                    folder, 'modules/{}/migrations'.format(folder)
            )

    return app

app = create_app()

alembic = Alembic()
alembic.init_app(app)