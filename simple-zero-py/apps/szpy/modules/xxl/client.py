# !/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Callable

import httpx

from .apis import *
from .model import CallbackIn, XXLConfig
from ...config.data_source import BaseConfig
from ...constants import status
from ...exception.model import xxl


class XXLClient:
    """
    用于管理本地方法注册映射, 注册, 回调, 取消注册
    """
    xxl_name: str = None
    config: XXLConfig
    runners: dict[str, Callable] = {}

    def __init__(self, *, config: XXLConfig = None):
        self.init(config)

    def header(self):
        return {'XXL-JOB-ACCESS-TOKEN': self.config.token}

    def register(self, *, name):
        self.xxl_name = name
        api = register.model_copy(update={
            'url': f'{self.config.server_addr.rstrip("/")}/{register.url.lstrip("/")}',
            'json_': {
                "registryGroup": "EXECUTOR",  # 固定值
                "registryKey": name,  # 执行器AppName
                "registryValue": self.config.registry_addr  # 执行器地址，内置服务跟地址
            },
            'headers': self.header()
        })
        resp = httpx.request(**api.model_dump())
        print(f'xxl-job: {self.xxl_name} registry result: {resp.json()}, conf: {self.config.model_dump()}')

    def unregister(self):
        api = unregister.model_copy(update={
            'url': f'{self.config.server_addr.rstrip("/")}/{unregister.url.lstrip("/")}',
            'json_': {
                "registryGroup": "EXECUTOR",  # 固定值
                "registryKey": self.xxl_name,  # 执行器AppName
                "registryValue": self.config.registry_addr  # 执行器地址，内置服务跟地址
            },
            'headers': self.header()
        })
        resp = httpx.request(**api.model_dump())
        print(f'xxl-job: {self.xxl_name} unregister result: {resp.json()}, conf: {self.config.model_dump()}')

    def callback(self, data: CallbackIn):
        api = call_back.model_copy(update={
            'url': f'{self.config.server_addr.rstrip("/")}/{call_back.url.lstrip("/")}',
            'json_': data,
            'headers': self.header()
        })
        resp = httpx.request(**api.model_dump())
        print(f'xxl-job log: {data.log_id}, result: {resp.json()}')

    def add_task(self, *, name: str, caller: Callable):
        self.runners[name] = caller

    def batch_add_task(self, data: dict[str, Callable]):
        self.runners = {**self.runners, **data}

    def get_task(self, name):
        runner = self.runners.get(name)
        if runner is None:
            raise xxl.TaskNoExist(f'task: {name} not exist!', code=status.STATUS_11000_XXL_TASK_NOT_EXIST)
        return runner

    def init(self, conf: XXLConfig = None):
        if self.xxl_name is not None:
            self.unregister()
        if conf is not None:
            self.config = conf
            self.register(name=conf.registry_name)

    def on_update(self, conf: BaseConfig):
        key = 'xxl'
        conf.register_changed_event(key, lambda: self.init(conf.xxl))


client: XXLClient = XXLClient()
