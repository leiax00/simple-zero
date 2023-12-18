# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from typing import Any

import aioredis
from fastapi import APIRouter, Depends

from szpy.config.app_config import app_conf
from szpy.entity.schema.resp import R
from szpy.modules.db import redis

router = APIRouter(prefix='/config', tags=['config'])


@router.get(
    '/props',
    response_model=R[Any],
    response_model_exclude_none=True
)
async def get_props():
    return R(data=app_conf)


@router.get(
    '/redis-test',
    response_model=R[Any],
    response_model_exclude_none=True
)
async def test_redis_get(client: aioredis.Redis = Depends(redis.aio_mgr.client)):
    data = await client.get('sys_config:sys.account.registerUser')
    return R(data=data)
