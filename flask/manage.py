import argparse
import subprocess
import os
import unittest
import flask_testing
from app import app, alembic


def run():
    if os.environ.get('ENV_TYPE') == 'prod':
        subprocess.call(
            ['gunicorn',
             '-c', 'default_configs/gunicorn_cfg.py',
             '--workers=4',
             '--bind',
             '0.0.0.0:5000',
             'src:app']
        )
    else:
        app.run(
            debug=True,
            host='0.0.0.0',
            port=5000,
        )

PARSER = argparse.ArgumentParser(description='Помощь')

PARSER.add_argument('--run', action='store_true', help='Запуск приложения')
PARSER.add_argument('--history', action='store_true', help='История миграций')
PARSER.add_argument('--upgrade', action='store_true', help='Накатить миграции')
PARSER.add_argument('--downgrade', action='store_true', help='Откатить миграции')
PARSER.add_argument('--test', action='store_true', help='Запустить тесты')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    if ARGS.run:
        run()
    elif ARGS.history:
        with app.app_context():
            print(alembic.log())
    elif ARGS.history:
        with app.app_context():
            alembic.log()
    elif ARGS.upgrade:
        with app.app_context():
            alembic.upgrade()
    elif ARGS.downgrade:
        with app.app_context():
            alembic.downgrade()
    elif ARGS.test:
        unittest.main()
    else:
        PARSER.print_help()