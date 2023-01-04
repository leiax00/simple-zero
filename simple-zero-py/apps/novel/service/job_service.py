# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from xxl_executor.Job import IJob
from xxl_executor.executor import XxlExecutor


class JobService(IJob):
    def __init__(self):
        super().__init__()

    def revert_join(self, executor: XxlExecutor):
        executor.join_batch({
            'add': self.add
        })

    def add(self, params_str):
        logging.info('hello, job!')
