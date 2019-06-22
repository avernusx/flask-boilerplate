import argparse
import subprocess
import os
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

PARSER = argparse.ArgumentParser(description='Manage instance.')

PARSER.add_argument('--run', action='store_true', help='Запуск приложения')
PARSER.add_argument('--history', action='store_true', help='История миграций')
PARSER.add_argument('--upgrade', action='store_true', help='Накатить миграции')
PARSER.add_argument('--downgrade', action='store_true', help='Откатить миграции')

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    if ARGS.run:
        run()
    if ARGS.history:
        with app.app_context():
            print(alembic.log())
    if ARGS.history:
        with app.app_context():
            alembic.log()
    if ARGS.upgrade:
        with app.app_context():
            alembic.upgrade()
    if ARGS.downgrade:
        with app.app_context():
            alembic.downgrade()