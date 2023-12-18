# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, BIGINT, VARCHAR, CHAR

from modules.novel.internal.entity.models.base import PGBase
from szpy.modules.db.sqlalchemy import SQLBase


class Author(SQLBase, PGBase):
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'author'

    id = Column(BIGINT, primary_key=True, index=True)
    platform = Column(BIGINT)
    author_id = Column(VARCHAR(64))
    platform_status = Column(CHAR(1))
    author_name = Column(VARCHAR(64))
    status = Column(CHAR(1), default='0')
