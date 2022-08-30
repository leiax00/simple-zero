# !/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import requests

from server.api import IApiManager, HttpMethod, Api


class ApiServer:
    def __init__(self, manager: IApiManager):
        self.manager = manager
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(self.manager.get_cookie())

    def req_limit(self):
        """ 限制  self.req_limit_time 秒钟一次请求 """
        delta = time.time() - self.manager.freq_manager.prev_req_time
        if delta < self.manager.freq_manager.freq_limit_by_time:
            time.sleep(self.manager.freq_manager.freq_limit_by_time - delta)
        self.manager.freq_manager.prev_req_time = time.time()

    def request(self, api: Api, json_: dict = None, data: dict = None, params: dict = None, **kwargs):
        self.req_limit()
        try:
            resp = self.session.request(**api.get_request_params(json_, data, params, **kwargs))
            resp.encoding = resp.apparent_encoding
            return resp
        except Exception as e:
            print(f'request error happen: {e}')
        return None

    def request_by_url(self, url: str, method: HttpMethod = HttpMethod.GET, headers=None, **kwargs):
        self.req_limit()
        kwargs = kwargs or {}
        json_obj = kwargs.get('json') or kwargs.get('json_')
        data = kwargs.get('data')
        params = kwargs.get('params')
        try:
            resp = self.session.request(method.value, url, headers=headers, json=json_obj, data=data,
                                        params=params)
            resp.encoding = resp.apparent_encoding
            return resp
        except Exception as e:
            print(f'request error happen: {e}')
        return None
