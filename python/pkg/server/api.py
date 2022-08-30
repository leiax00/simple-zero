# !/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
from enum import Enum


class HttpMethod(Enum):
    GET = 'GET'
    POST = 'POST'
    PUT = 'PUT'
    DELETE = 'DELETE'


class Domain(Enum):
    BI_QU_GE = 'https://www.xbiquwx.la'


class Header:
    def __init__(self, **kwargs):
        self.__dict__ = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/101.0.4951.64 Safari/537.36 Edg/101.0.1210.53 '
        }
        self.__dict__ = {**self.__dict__, **kwargs}

    def to_dict(self):
        return self.__dict__


class ICookie:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_cookies(self):
        raise NotImplementedError('Not Implemented')


class Api:
    default_domain: Domain or str = ''

    def __init__(self, uri, method: HttpMethod or str, domain: Domain or str = None, header=Header(), **kwargs):
        self.uri = uri
        domain = domain or Api.default_domain
        self.method = method if isinstance(method, str) else method.value
        self.domain = domain if isinstance(domain, str) else domain.value
        self.header = header
        self.__dict__ = {**kwargs, **self.__dict__}

    def with_params(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        return self

    def get_url(self, **kwargs):
        return f'{self.domain.rstrip("/")}/{self.uri.lstrip("/")}'.format(**(kwargs or {}))

    def get_request_params(self, json_=None, data=None, params=None, **kwargs):
        return {
            'method': self.method,
            'url': self.get_url(**kwargs),
            'json': json_,
            'data': data,
            'params': params,
            'headers': self.header.to_dict()
        }


class ApiMap:
    def __init__(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}

    def with_dict(self, **kwargs):
        self.__dict__ = {**self.__dict__, **kwargs}
        return self


class IApiManager:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.freq_manager = FreqManager()

    @abc.abstractmethod
    def get_cookie(self):
        raise NotImplementedError('Not Implemented')


class FreqManager:
    def __init__(self, **kwargs):
        self.freq_limit_by_time = kwargs.get('freq_limit_by_time') or 5
        self.prev_req_time = 0
