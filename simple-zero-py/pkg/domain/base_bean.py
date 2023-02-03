# !/usr/bin/env python
# -*- coding: utf-8 -*-


class BaseBean:
    def with_dict(self, params: dict):
        self.__dict__ = {**self.__dict__, **params}
        return self
