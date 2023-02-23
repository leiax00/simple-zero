# !/usr/bin/env python
# -*- coding: utf-8 -*-
import re

from peewee import Model
from playhouse.shortcuts import model_to_dict


class BaseBean:
    def with_dict(self, params: dict):
        self.__dict__ = {**self.__dict__, **params}
        return self


class BaseModelBean(Model, BaseBean):
    def to_camel_dict(self):
        origin_dict = model_to_dict(self)
        tmp = {}
        for k, v in origin_dict.items():
            tmp[re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), k.lower())] = v
        return tmp

    class Meta:
        pass
