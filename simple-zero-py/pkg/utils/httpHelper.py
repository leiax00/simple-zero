# !/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
from enum import Enum

import aiohttp
import chardet
import requests


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Header:
    def __init__(self, **kwargs):
        self.__dict__ = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53 '
        }
        self.__dict__ = {**self.__dict__, **kwargs}

    def to_dict(self):
        return self.__dict__


class Api:
    def __init__(self, uri, method: HttpMethod or str, domain=None, header=Header(), **kwargs):
        self.uri = uri
        self.domain = domain or ''
        self.method = method if isinstance(method, str) else method.value
        self.header = header
        self.__dict__ = {**kwargs, **self.__dict__}

    def with_params(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        return self

    def get_url(self, **kwargs):
        return f'{self.domain.strip("/")}/{self.uri.strip("/")}'.format(**(kwargs or {}))

    def get_request_params(self, json_=None, data=None, params=None, **kwargs):
        return {
            'method': self.method,
            'url': self.get_url(**kwargs),
            'json': json_,
            'data': data,
            'params': params,
            'headers': self.header.to_dict()
        }


class FreqManager:
    def __init__(self, **kwargs):
        self.freq_limit_by_time = kwargs.get('freq_limit_by_time') or 5
        self.prev_req_time = 0


class IApiManager:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.freq_manager = FreqManager()


class HttpSession(requests.Session):
    def __init__(self, prefix_url='', *args, **kwargs):
        super(HttpSession, self).__init__(*args, **kwargs)
        self.base_url = prefix_url.rstrip("/")

    def request(self, method: str, url, **kwargs):
        url = f'{self.base_url}/{url}' if not url.startswith('http') else url
        return super(HttpSession, self).request(method, url, **kwargs)


class AioHttpClient:
    def __init__(self, prefix_url='', client=None):
        self.__client = client
        self.base_url = prefix_url.strip("/")

    def session(self) -> aiohttp.ClientSession:
        if self.__client is None:
            self.__client = aiohttp.ClientSession()
        return self.__client

    def _url(self, url: str) -> str:
        return f'{self.base_url}/{url.strip("/")}'

    def request(self, method: str, url, **kwargs):
        return self.session().request(method, self._url(url), **kwargs)


def content(resp):
    encoding = chardet.detect(resp.content)['encoding']
    return resp.content.decode(encoding)
