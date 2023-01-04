# !/usr/bin/env python
# -*- coding: utf-8 -*-


class XxlConfig:
    def __init__(self):
        self.admin_url = None
        self.access_token = None
        self.executor_name = None
        self.registry_url = None

    def fill(self, params: dict = {}):
        self.__dict__ = {**self.__dict__, **params}
        return self
