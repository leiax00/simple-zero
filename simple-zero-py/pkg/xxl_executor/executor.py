# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
from enum import Enum

from flask import g

from utils.httpHelper import AioHttpClient, Api, HttpMethod, Header
from xxl_executor.Job import IJob
from xxl_executor.config import XxlConfig


class XxlApi(Enum):
    call_back = Api('/api/callback', HttpMethod.POST)
    register = Api('/api/registry', HttpMethod.POST)
    remove = Api('/api/registryRemove', HttpMethod.POST)


class XxlExecutor:
    def __init__(self, conf: dict):
        self.conf = XxlConfig().fill(conf)
        self.client = AioHttpClient(self.conf.admin_url)
        self._header = Header(**{
            'XXL-JOB-ACCESS-TOKEN': self.conf.access_token
        })
        self._jobs = {}

    def _api(self, api: XxlApi):
        return api.value.with_params(header=self._header)

    def task_callback(self, job_name, job_params, **kwargs):
        return self.execute(job_name, job_params)

    async def register(self):
        params = self._api(XxlApi.register).get_request_params({
            'registryGroup': 'EXECUTOR',
            'registryKey': self.conf.executor_name,
            'registryValue': self.conf.registry_url,
        })
        async with self.client.request(**params) as resp:
            print(f'xxl-job registry result: {await resp.json()}')

    async def remove(self):
        params = self._api(XxlApi.remove).get_request_params({
            'registryGroup': 'EXECUTOR',
            'registryKey': self.conf.executor_name,
            'registryValue': self.conf.registry_url,
        })
        async with self.client.request(**params) as resp:
            print(f'xxl-job remove registry result: {await resp.json()}')

    def join(self, job: IJob):
        job.revert_join(self)
        return self

    def join_batch(self, jobs={}):
        self._jobs = {**self._jobs, **jobs}
        return self

    def execute(self, job_name, job_params):
        job = self._jobs.get(job_name)
        if job is None:
            print(f'no such job: {job_name}')
            return False
        return job(job_params)


async def init_xxl(xxl: XxlApi, job: IJob):
    xxl.join(job)
    await asyncio.gather(asyncio.create_task(xxl.register()))
