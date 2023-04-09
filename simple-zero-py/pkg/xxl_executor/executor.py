# !/usr/bin/env python
# -*- coding: utf-8 -*-
import asyncio
import logging
import threading
from enum import Enum
from queue import Queue
from time import sleep

import aiohttp
import requests

from utils.async_utils import async_run, get_loop
from utils.httpHelper import Api, HttpMethod, Header
from xxl_executor.Job import IJob
from xxl_executor.config import XxlConfig, XxlTask


class XxlApi(Enum):
    call_back = Api('/api/callback', HttpMethod.POST)
    register = Api('/api/registry', HttpMethod.POST)
    remove = Api('/api/registryRemove', HttpMethod.POST)


class XxlExecutor:
    def __init__(self, conf: dict):
        self.conf = XxlConfig().fill(conf)
        self._header = Header(**{
            'XXL-JOB-ACCESS-TOKEN': self.conf.access_token
        })
        self._jobs = {}
        self._running_jobs = []
        self.start_model()

    def _api(self, api: XxlApi):
        return api.value.with_params(domain=self.conf.admin_url, header=self._header)

    def task_callback(self, rst, task: XxlTask):
        is_failed = isinstance(rst, str)
        code = 200 if not is_failed else 500
        params = self._api(XxlApi.call_back).get_request_params([{
            'logId': task.log_id,
            'logDateTim': task.log_time,
            'handleCode': code,
            'handleMsg': f'{rst if is_failed else "Execute OK!"}',
        }])
        with requests.request(**params) as resp:
            logging.info(f'xxl-job: {task.job_id} callback rst: {resp.json()}')

    async def register(self):
        params = self._api(XxlApi.register).get_request_params({
            'registryGroup': 'EXECUTOR',
            'registryKey': self.conf.executor_name,
            'registryValue': self.conf.registry_url,
        })
        async with aiohttp.request(**params) as resp:
            logging.info(f'xxl-job registry result: {await resp.json()}')

    async def remove(self):
        params = self._api(XxlApi.remove).get_request_params({
            'registryGroup': 'EXECUTOR',
            'registryKey': self.conf.executor_name,
            'registryValue': self.conf.registry_url,
        })
        async with aiohttp.request(**params) as resp:
            logging.info(f'xxl-job remove registry result: {await resp.json()}')

    def join(self, job: IJob):
        job.revert_join(self)
        return self

    def join_batch(self, jobs: dict):
        self._jobs = {**self._jobs, **jobs}
        return self

    def execute(self, task: XxlTask):
        def execute_job():
            logging.info(f'start to execute task: {task}')
            rst = True
            try:
                if task.glue_type != 'BEAN':
                    rst = f'current executor only support GLUE TYPE: BEAN, but real type: {task.glue_type}'
                job = self._jobs.get(task.job_name)
                if job is None:
                    rst = f'no such job or job not registry: {task.job_name}'
                else:
                    rst = job(task.job_params)
            finally:
                self.task_callback(rst, task)
                logging.info(f'end to execute task! job_id: {task.job_id}, log_id: {task.log_id}, result: {rst}')
            return rst

        execute_job()

    def produce_task(self, task: XxlTask):
        self._running_jobs.append(task)
        logging.info(f'push task to execute list, task: {task}')

    def consume_task(self):
        while True:
            try:
                if len(self._running_jobs) > 0:
                    jobs, self._running_jobs = self._running_jobs, []
                    for job in jobs:
                        threading.Thread(target=self.execute, args=(job,), daemon=True,
                                         name=f'xxl-job-{job.job_id}').start()
                else:
                    sleep(self.conf.consume_period)
            except Exception as e:
                logging.error(e)

    def start_model(self):
        threading.Thread(target=self.consume_task, daemon=True, name='xxl-job-consumer').start()


async def init_xxl(xxl: XxlExecutor, job: IJob):
    xxl.join(job)
    await asyncio.gather(asyncio.create_task(xxl.register()))
