# !/usr/bin/env python
# -*- coding: utf-8 -*-
import queue
import re


def to_camel_dict(origin_dict: dict):
    tmp = {}
    for k, v in origin_dict.items():
        tmp_v = v
        if isinstance(v, dict):
            tmp_v = to_camel_dict(v)
        if isinstance(v, list) or isinstance(v, set):
            tmp_v = to_camel_list(v)

        tmp[re.sub('_([a-zA-Z])', lambda m: (m.group(1).upper()), k)] = tmp_v
    return tmp


def to_camel_list(origin: list):
    tmp = []
    for item in origin:
        if isinstance(item, list):
            tmp.append(to_camel_list(item))
        if isinstance(item, dict):
            tmp.append(to_camel_dict(item))
        else:
            tmp.append(item)
    return tmp
