import asyncio
import logging

from flask import Flask, g
from gevent import pywsgi

import config
from config import db
from extender.flask_extender import *
from jobs.job_service import JobService
from routes.api import api
from xxl_executor.executor import init_xxl
from xxl_executor.routes import api as xxl_api

SERVER_PREFIX = '/api/novel'

init_logger()

app = Flask(__name__)
app.json = SelfJsonProvider(app)
# 允许格式: [api] , [url_prefix, api]
register_route(app, api, SERVER_PREFIX)
register_route(app, xxl_api, force_prefix=True)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


host = config.config.get('host')
port = config.config.get('port')
logging.info(f'\n\n{"*" * 100}\nserver start on: {host}:{port}\n{"*" * 100}\n\n')
asyncio.run(init_xxl(config.xxl, JobService()))

if __name__ == '__main__':
    # app.config.from_mapping({'CUSTOM': Config.__dict__})  # CUSTOM必须大写
    # app.run('0.0.0.0', 11000, debug=True)

    server = pywsgi.WSGIServer((host, port), app)
    server.serve_forever()
