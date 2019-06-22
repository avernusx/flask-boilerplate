import argparse
import subprocess
import os
from app import app


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

if __name__ == '__main__':
    ARGS = PARSER.parse_args()
    if ARGS.run:
        run()