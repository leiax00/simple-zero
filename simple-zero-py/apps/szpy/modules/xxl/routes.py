# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Annotated

from fastapi import APIRouter, Header, status

from szpy.entity.schema.resp import R, RBase
from szpy.modules.xxl.model import XXLObjBase, LogIn, R1, XXLObj

router = APIRouter(prefix='/xxl', tags=['xxl-job'])


@router.get(
    '/beat',
    response_model=R[str],
    name='心跳检测',
    description='xxl-job心跳检测'
)
def heart_beat():
    return RBase(code=status.HTTP_200_OK)


@router.post(
    '/idleBeat',
    response_model=R[str],
    description='说明：调度中心检测指定执行器上指定任务是否忙碌（运行中）时使用'
)
def idle_beat(
        data: XXLObjBase,
        token: Annotated[str, Header(alias='XXL-JOB-ACCESS-TOKEN')] = None
):
    """
    说明：调度中心检测指定执行器上指定任务是否忙碌（运行中）时使用
    """
    print(data.model_dump(), token)
    return RBase(code=status.HTTP_200_OK)


@router.post(
    '/run',
    response_model=R[str],
    description='说明：触发任务执行'
)
def run(
        data: XXLObj,
        token: Annotated[str, Header(alias='XXL-JOB-ACCESS-TOKEN')] = None
):
    """
    说明：触发任务执行
    """
    print(data.model_dump(), token)
    return RBase(code=status.HTTP_200_OK)


@router.post(
    '/kill',
    response_model=R[str],
    description='说明：终止任务'
)
def idle_beat(
        data: XXLObjBase,
        token: Annotated[str, Header(alias='XXL-JOB-ACCESS-TOKEN')] = None
):
    """
    说明：终止任务
    """
    print(data.model_dump(), token)
    return RBase(code=status.HTTP_200_OK)


@router.post(
    '/log',
    response_model=R1,
    description='说明: 加载日志'
)
def get_log(
        data: LogIn,
        token: Annotated[str, Header(alias='XXL-JOB-ACCESS-TOKEN')] = None
):
    print(data.model_dump(), token)
    return
