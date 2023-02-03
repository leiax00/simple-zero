# !/usr/bin/env python
# -*- coding: utf-8 -*-
from domain.base_bean import BaseBean


class SubscribeInfo(BaseBean):
    def __init__(self):
        self.bid = None
        self.cid = None
        self.group = None
