# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import typing as t
from typing import Union

from flask.json.provider import DefaultJSONProvider

from extender.serial_extender import MyEncoder


class API(object):
    def __init__(self, api, prefix=None):
        self.prefix = prefix
        self.api = api


class SelfJsonProvider(DefaultJSONProvider):
    ensure_ascii = False

    cls = MyEncoder

    def dumps(self, obj: t.Any, **kwargs: t.Any) -> str:
        kwargs.setdefault("cls", self.cls)
        kwargs.setdefault("ensure_ascii", self.ensure_ascii)
        kwargs.setdefault("sort_keys", self.sort_keys)
        return json.dumps(obj, **kwargs)

    def loads(self, s: Union[str, bytes], **kwargs: t.Any) -> t.Any:
        kwargs.setdefault("cls", self.cls)
        return json.loads(s, **kwargs)
