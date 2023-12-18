# !/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import contextmanager, asynccontextmanager
from typing import Optional

import aioredis
import redis
from pydantic import BaseModel

from szpy.config.data_source import BaseConfig


class RedisConfig(BaseModel):
    host: Optional[str] = None
    port: Optional[int] = 6379
    decode_responses: bool = True
    db: int = 0
    max_connections: int = 10


class RedisManager:
    config: RedisConfig = None
    __redis = None

    def __init__(self, config: RedisConfig = None):
        self.init(config)

    def init(self, config: RedisConfig):
        if config is None:
            return

        self.config = config
        self.__redis = redis.from_url(
            f'redis://{config.host}:{config.port}',
            encoding="utf-8",
            decode_responses=self.config.decode_responses,
            db=self.config.db,
            max_connections=self.config.max_connections or 10
        )

    def client(self) -> redis.Redis:
        return self.__redis

    def on_update(self, conf: BaseConfig):
        key = 'redis'
        conf.register_changed_event(key, lambda: self.init(conf.redis))


class AioRedisManager:
    config: RedisConfig = None
    __redis = None

    def __init__(self, config: RedisConfig = None):
        self.init(config)

    def init(self, config: RedisConfig = None):
        if config is None:
            return

        self.config = config
        self.__redis = aioredis.from_url(
            f'redis://{config.host}:{config.port}',
            encoding="utf-8",
            decode_responses=self.config.decode_responses,
            db=self.config.db,
            max_connections=self.config.max_connections or 10
        )

    async def client(self) -> aioredis.Redis:
        return self.__redis

    def on_update(self, conf: BaseConfig):
        key = 'redis'
        conf.register_changed_event(key, lambda: self.init(conf.redis))


mgr = RedisManager()
aio_mgr = AioRedisManager()
