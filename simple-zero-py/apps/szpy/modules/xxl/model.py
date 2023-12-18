# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from pydantic import BaseModel, Field

from szpy.entity.schema.resp import RBase


class XXLConfig(BaseModel):
    server_addr: str
    token: str = 'default_token'
    registry_addr: str
    registry_name: str = 'xxl-sz-novel'


class XXLObjBase(BaseModel):
    job_id: Optional[str] = Field(default=None, alias='jobId')


class XXLObj(XXLObjBase):
    handler: Optional[str] = Field(default=None, alias='executorHandler')
    params: Optional[str] = Field(default=None, alias='executorParams')
    block_strategy: Optional[str] = Field(default=None, alias='executorBlockStrategy')
    timeout: Optional[int] = Field(default=0, alias='executorTimeout')
    log_id: Optional[int] = Field(default=None, alias='logId')
    log_time: Optional[int] = Field(default=None, alias='logDateTime')
    glue_type: Optional[str] = Field(default='BEAN', alias='glueType')
    glue_source: Optional[str] = Field(default=None, alias='glueSource')
    glue_update_time: Optional[int] = Field(default=None, alias='glueUpdatetime')
    broadcast_index: Optional[int] = Field(default=None, alias='broadcastIndex')
    broadcast_total: Optional[int] = Field(default=None, alias='broadcastTotal')


class LogIn(BaseModel):
    start_time: Optional[int] = Field(default=None, alias='logDateTim')
    log_id: Optional[int] = Field(default=None, alias='logId')
    from_line_num: Optional[int] = Field(default=None, alias='fromLineNum')


class LogOut(BaseModel):
    from_line_num: Optional[int] = Field(default=None, alias='fromLineNum')
    to_line_num: Optional[int] = Field(default=None, alias='toLineNum')
    content: Optional[str] = Field(default=None, alias='logContent')
    is_end: Optional[int] = Field(default=None, alias='isEnd')


class R1(RBase):
    content: Optional[LogOut] = None


class CallbackIn(BaseModel):
    log_id: Optional[int] = Field(default=None, alias='logId', description='本次调度日志ID')
    exec_time: Optional[int] = Field(default=None, alias='logDateTim', description='本次调度日志时间')
    code: Optional[int] = Field(default=None, alias='handleCode', description='200 表示任务执行正常，500表示失败')
    msg: Optional[str] = Field(default=None, alias='handleMsg', description='失败时的信息')
