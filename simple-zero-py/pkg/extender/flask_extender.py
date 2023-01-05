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
        # kwargs.setdefault("cls", self.cls)
        return json.loads(s, **kwargs)


def init_logger():
    dictConfig({
        'version': 1,
        'formatters': {'default': {
            'format': '[%(asctime)s %(levelname)s] %(message)s -- [%(module)s.%(funcName)s(line:%(lineno)d)]',
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


def register_routes(app, api_list, prefix='/', force_prefix=False):
    for item in api_list:
        register_route(app, item, prefix, force_prefix)


def register_route(app, api, prefix='/', force_prefix=False):
    """
    注册api
    :param app: flask应用app
    :param api: 要注册的API集合, Blueprint, 为元组时, 第一个为api的prefix, 第二个为api, 否则为api
    :param prefix: api前缀
    :param force_prefix: 是否强制使用prefix作为前缀, 否则为 prefix/{api[0] | api.name}
    :return:
    """
    if (isinstance(api, tuple) or isinstance(api, list)) and len(api) >= 2:
        prefix = f'{prefix}/{api[0]}' if not force_prefix else f'{prefix}'
        api.url_prefix = prefix
        app.register_blueprint(api[1])
    else:
        prefix = f'{prefix}/{api.name}' if not force_prefix else f'{prefix}'
        api.url_prefix = prefix
        app.register_blueprint(api)
