# !/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Optional

from fastapi import Query
from pydantic import BaseModel, Field


class BaseVO(BaseModel):
    create_time: datetime = Field(default=datetime.now(), description='创建时间')
    create_by: Optional[str] = Field(default=None, description='创建者')
    update_time: Optional[datetime] = Field(default=None, description='更新时间')
    update_by: Optional[str] = Field(default=None, description='更新者')


class Remark(BaseModel):
    remark: Optional[str] = Field(default=None, description='备注信息')
