# !/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import VARCHAR, Column, TEXT
from sqlalchemy.dialects.postgresql import TIMESTAMP


class PGBase:
    create_time = Column(TIMESTAMP)
    create_by = Column(VARCHAR(64))
    update_time = Column(TIMESTAMP)
    update_by = Column(VARCHAR(64))


class Remark:
    remark = Column(TEXT)
