# !/usr/bin/env python
# -*- coding: utf-8 -*-
import abc
from typing import Optional, Callable

from pydantic import BaseModel, Field


class SourceData(BaseModel):
    content: Optional[str]


class BaseConfig(BaseModel):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def update(self, conf_str: str):
        raise NotImplementedError('No Implemented!')

    @abc.abstractmethod
    def register_data_source(self, getter, listen=True):
        raise NotImplementedError('No Implemented!')

    @abc.abstractmethod
    def register_changed_event(self, root_key: str, callback: Callable):
        raise NotImplementedError('No Implemented!')


class DataGetter:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_data(self) -> SourceData:
        raise NotImplementedError('No Implemented!')

    @abc.abstractmethod
    def listen_data(self, callback: Callable[[SourceData], None]):
        raise NotImplementedError('No Implemented!')


class ProxyConfig(BaseModel):
    username: Optional[str] = Field(default=None, description='公共的代理用户名')
    password: Optional[str] = Field(default=None, description='公共的代理用户密码')
    maxThreadCount: int = Field(default=1, description='代理允许的最大并发数, 结合业务和代理数量总和考虑')
    maxRetryCount: int = Field(default=3, description='代理使用过程中单线程的最大重试次数, 增加业务成功率')
    retryPeriod: int = Field(default=2, description='失败时的重试时间间隔, 单位: 秒')
    addresses: list[str] = Field(default=[], description='代理列表, ip:port或者user:password@ip:port')

    def req_proxy(self, addr_index):
        proxy_count = len(self.addresses)
        if proxy_count == 0:
            return addr_index, None
        if proxy_count == addr_index:
            return 0, None

        p = self.addresses[addr_index]
        addr_index += 1
        if self.username is None:
            return addr_index, {
                "http://": f"http://{p}",
                "https://": f"http://{p}",
            }
        return addr_index, {
            "http://": f"http://{self.username}:{self.password}@{p}",
            "https://": f"http://{self.username}:{self.password}@{p}",
        }
