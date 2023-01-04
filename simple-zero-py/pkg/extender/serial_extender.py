# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
from enum import Enum
from json import JSONEncoder, JSONDecoder


class MyEncoder(JSONEncoder):
    def default(self, obj):
        # if isinstance(obj, ObjectId):
        #     return str(obj)
        if isinstance(obj, Serialize):
            return obj.__dict__
        elif isinstance(obj, Enum):
            return obj.value
        elif isinstance(obj, object) and hasattr(obj, '__dict__'):
            return obj.__dict__
        else:
            return JSONEncoder.default(self, obj)


class Serialize(object):
    def __str__(self):
        return json.dumps(self.__dict__, cls=MyEncoder, ensure_ascii=False)

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        return json.loads(self.__str__())


if __name__ == '__main__':
    test_str = b'{\r\n    "jobId": 43\r\n}'
    test_str = '{"jobId":43}'
    print(json.loads(test_str))
