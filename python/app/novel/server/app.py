from flask import Flask
from gevent import pywsgi

from extender.flask_extender import *
from routes.api import api

SERVER_PREFIX = '/novel/v1'
# 允许格式: api , (url_prefix, api)
apis = [
    api
]


app = Flask(__name__)
app.json = SelfJsonProvider(app)
init_logger()
register_routes(app, SERVER_PREFIX, apis)

if __name__ == '__main__':
    # app.config.from_mapping({'CUSTOM': Config.__dict__})  # CUSTOM必须大写
    server = pywsgi.WSGIServer(('0.0.0.0', 11000), app)
    server.serve_forever()
