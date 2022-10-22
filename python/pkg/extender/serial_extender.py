# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from enum import Enum
from json import JSONEncoder

from bson import ObjectId


class MyEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        if isinstance(obj, Serialize):
            return obj.__dict__
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, object) and hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return obj


class Serialize(object):
    def __str__(self):
        return json.dumps(self.__dict__, cls=MyEncoder, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return json.loads(self.__str__())
