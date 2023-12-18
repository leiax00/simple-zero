# !/usr/bin/env python
# -*- coding: utf-8 -*-

from config import db
from domain.base_bean import BaseModelBean


class BaseModel(BaseModelBean):
    class Meta:
        database = db
        schema = 'novel'
