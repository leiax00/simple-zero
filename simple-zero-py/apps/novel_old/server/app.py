from logging.config import dictConfig

from flask import Flask
from gevent import pywsgi

from conf.config import Config
from extender.flask_extender import SelfJsonProvider
from routes.api import api

SERVER_PREFIX = Config.url_prefix


def init_logger():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }},
        'handlers': {
            'wsgi': {
                'class': 'logging.StreamHandler',
                'stream': 'ext://flask.logging.wsgi_errors_stream',
                'formatter': 'default'
            },
            'file': {
                'class': 'logging.FileHandler',
                'level': 'INFO',
                'filename': 'server.log',
                'formatter': 'default'
            }
        },
        'root': {
            'level': 'INFO',
            'handlers': ['file']  # 如果要打印在控制台, 加上 wsgi
        }
    })


def register_routes():
    # 允许格式: api , (url_prefix, api)
    api_list = [
        api
    ]

    for item in api_list:
        if (isinstance(item, tuple) or isinstance(item, list)) and len(item) >= 2:
            app.register_blueprint(item[1], url_prefix=f'{SERVER_PREFIX}/{item[0]}')
        else:
            item.url_prefix = f'{SERVER_PREFIX}/{item.name}'
            app.register_blueprint(item)


app = Flask(__name__)
app.json = SelfJsonProvider(app)
init_logger()
register_routes()

if __name__ == '__main__':
    # app.config.from_mapping({'CUSTOM': Config.__dict__})  # CUSTOM必须大写
    server = pywsgi.WSGIServer((Config.host, Config.port), app)
    server.serve_forever()
