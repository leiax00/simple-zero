# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import os
from functools import lru_cache
from typing import Optional, Callable

import nacos
from nacos import NacosClient
from pydantic.v1 import BaseSettings

from szpy.config.data_source import SourceData, DataGetter


class NacosConfig(BaseSettings):
    nacos_addr: str = '10.1.0.7:8848'
    nacos_ns: Optional[str] = None
    nacos_props_group: str = 'DEFAULT_GROUP'
    nacos_props_id: str = 'sz-novel.yaml'


class NacosManager(DataGetter):
    config: NacosConfig
    client: NacosClient

    def __init__(self, config: NacosConfig):
        self.config = config
        self.client = nacos.NacosClient(config.nacos_addr, namespace=config.nacos_ns,
                                        logDir=os.path.join(os.getcwd(), 'logs', 'nacos'))
        # 禁用快照存储, 否则配置监听的内部机制导致快照生成
        self.client.no_snapshot = True
        # nacos的第三方库0.1.14的日志打印混乱, 真实环境中设置高级别的日志等级
        logger = logging.getLogger('nacos')
        logger.setLevel(logging.WARNING)
        # self.client.set_debugging()

    def get_data(self) -> SourceData:
        def config(data_id) -> str | None:
            return self.client.get_config(data_id, self.config.nacos_props_group)

        c = config(self.config.nacos_props_id)
        if c is not None:
            return SourceData(content=c)

    def listen_data(self, callback: Callable[[SourceData], None]):
        def c_wrapper(c_dict: dict):
            callback(SourceData(**c_dict))
        self.client.add_config_watchers(
            self.config.nacos_props_id,
            self.config.nacos_props_group,
            [c_wrapper]
        )


@lru_cache()
def nacos_manager():
    return NacosManager(NacosConfig())


if __name__ == '__main__':
    os.environ['DATA_ID'] = 'application-dev.yaml'
    m = nacos_manager()
    for item in m.fill_config():
        print(item)
