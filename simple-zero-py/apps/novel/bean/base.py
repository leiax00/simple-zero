# !/usr/bin/env python
# -*- coding: utf-8 -*-
from peewee import *

from config import db
from domain.base_bean import BaseBean


class BaseModel(Model, BaseBean):
    class Meta:
        database = db
        schema = 'novel'
