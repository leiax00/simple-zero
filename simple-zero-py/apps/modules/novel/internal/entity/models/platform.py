# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import Column, BIGINT, VARCHAR, CHAR

from modules.novel.internal.entity.models.base import PGBase
from szpy.modules.db.sqlalchemy import SQLBase


class Platform(SQLBase, PGBase):
    """
    平台定义表
    """
    __table_args__ = {'schema': 'novel'}
    __tablename__ = 'platform'

    id = Column(BIGINT, primary_key=True, index=True)
    platform_name = Column(VARCHAR(64))
    nick_name = Column(VARCHAR(64))
    status = Column(CHAR(1), default='0')
