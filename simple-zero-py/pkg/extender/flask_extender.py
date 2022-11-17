# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import typing as t
from logging.config import dictConfig
from typing import Union

from flask.json.provider import DefaultJSONProvider

from extender.serial_extender import MyEncoder


class API(object):
    def __init__(self, api, prefix=None):
        self.prefix = prefix
        self.api = api


class SelfJsonProvider(DefaultJSONProvider):
    ensure_ascii = False

    cls = MyEncoder

    def dumps(self, obj: t.Any, **kwargs: t.Any) -> str:
        kwargs.setdefault("cls", self.cls)
        kwargs.setdefault("ensure_ascii", self.ensure_ascii)
        kwargs.setdefault("sort_keys", self.sort_keys)
        return json.dumps(obj, **kwargs)

    def loads(self, s: Union[str, bytes], **kwargs: t.Any) -> t.Any:
        kwargs.setdefault("cls", self.cls)
        return json.loads(s, **kwargs)


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
            'handlers': ['file', 'wsgi']  # 如果要打印在控制台, 加上 wsgi
        }
    })


def register_routes(app, prefix, api_list):
    for item in api_list:
        if (isinstance(item, tuple) or isinstance(item, list)) and len(item) >= 2:
            app.register_blueprint(item[1], url_prefix=f'{prefix}/{item[0]}')
        else:
            item.url_prefix = f'{prefix}/{item.name}'
            app.register_blueprint(item)
