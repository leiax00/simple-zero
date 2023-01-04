import asyncio

from flask import Flask, g
from gevent import pywsgi

import config
from config import db
from extender.flask_extender import *
from routes.api import api
from service.job_service import JobService
from xxl_executor.executor import init_xxl
from xxl_executor.routes import api as xxl_api

SERVER_PREFIX = '/novel/v1'

app = Flask(__name__)
app.json = SelfJsonProvider(app)


@app.before_request
def before_request():
    g.db = db
    g.db.connect()


@app.after_request
def after_request(response):
    g.db.close()
    return response


init_logger()

# 允许格式: [api] , [url_prefix, api]
register_route(app, api, SERVER_PREFIX)
register_route(app, xxl_api, force_prefix=True)
asyncio.run(init_xxl(config.xxl, JobService()))

if __name__ == '__main__':
    # app.config.from_mapping({'CUSTOM': Config.__dict__})  # CUSTOM必须大写

    server = pywsgi.WSGIServer(('0.0.0.0', 11000), app)
    server.serve_forever()
