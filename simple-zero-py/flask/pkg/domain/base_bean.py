# !/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import Model
from playhouse.shortcuts import model_to_dict

from utils.common_utils import to_camel_dict


class BaseBean:
    def with_dict(self, params: dict):
        self.__dict__ = {**self.__dict__, **params}
        return self


class BaseModelBean(Model, BaseBean):
    def to_camel_dict(self):
        origin_dict = model_to_dict(self)
        return to_camel_dict(origin_dict)

    class Meta:
        pass
