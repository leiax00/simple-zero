# !/usr/bin/env python
# -*- coding: utf-8 -*-
from bean.book_domain import Serialize


class Response(Serialize):
    def __init__(self):
        self.code = 0
        self.msg = ''
        self.data = None

    def fill(self, code=0, msg='', data=None):
        self.code = code
        self.msg = msg
        self.data = data
        return self

    def with_ok(self, data):
        self.data = data
        return self


