# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional, Callable

import yaml

from szpy.config.data_source import BaseConfig, SourceData, DataGetter, ProxyConfig
from szpy.modules.db.redis import RedisConfig
from szpy.modules.db.sqlalchemy import DBConfig
from szpy.modules.xxl.model import XXLConfig


class AppConfig(BaseConfig):
    __data_sources: list[DataGetter] = []
    __changed_events: dict[str, list[Callable]] = {}
    xxl: Optional[XXLConfig] = None
    db: Optional[DBConfig] = None
    redis: Optional[RedisConfig] = None
    proxy: Optional[ProxyConfig] = None

    def update(self, new_c: SourceData):
        yaml_conf = new_c.content
        if yaml_conf is None:
            return

        new_conf = yaml.load(yaml_conf, Loader=yaml.FullLoader)
        self._set_xxl(new_conf, 'xxl')
        self._set_db(new_conf, 'db')
        self._set_redis(new_conf, 'redis')
        self._set_proxy(new_conf, 'proxy')

    def register_data_source(self, getter: DataGetter, listen=True):
        self.update(getter.get_data())
        listen and getter.listen_data(self.update)
        self.__data_sources.append(getter)

    def register_changed_event(self, root_key: str, callback: Callable):
        events = self.__changed_events.get(root_key, [])
        events.append(callback)
        self.__changed_events[root_key] = events
        callback()

    def _set_xxl(self, new_c: dict, root_key: str):
        xxl_conf = new_c.get(root_key)
        if xxl_conf is not None:
            if self.xxl is None:
                self.xxl = XXLConfig(**xxl_conf)
            else:
                self.xxl = self.xxl.model_copy(update=xxl_conf)
            self._dispatch_events(root_key)

    def _set_db(self, new_c: dict, root_key: str):
        conf = new_c.get(root_key)
        if conf is not None:
            if self.db is None:
                self.db = DBConfig(**conf)
            else:
                self.db = self.db.model_copy(update=conf)
            self._dispatch_events(root_key)

    def _set_redis(self, new_c: dict, root_key: str):
        conf = new_c.get(root_key)
        if conf is not None:
            if self.redis is None:
                self.redis = RedisConfig(**conf)
            else:
                self.redis = self.redis.model_copy(update=conf)
            self._dispatch_events(root_key)

    def _set_proxy(self, new_c: dict, root_key: str):
        conf = new_c.get(root_key)
        if conf is not None:
            if self.proxy is None:
                self.proxy = ProxyConfig(**conf)
            else:
                self.db = self.db.model_copy(update=conf)
            self._dispatch_events(root_key)

    def _dispatch_events(self, root_key: str):
        try:
            events = self.__changed_events.get(root_key)
            if events and len(events) > 0:
                for event in events:
                    event()
        except Exception as e:
            pass


app_conf = AppConfig()
