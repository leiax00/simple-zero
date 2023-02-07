# !/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from service.j2wx_stat import j2wx
from service.service import novel
from xxl_executor.Job import IJob
from xxl_executor.executor import XxlExecutor


class JobService(IJob):
    def __init__(self):
        super().__init__()
        self.novel = novel
        self.j2wx = j2wx

    def revert_join(self, executor: XxlExecutor):
        executor.join_batch({
            '测试add': self.add,
            '更新书架': self.update_bookshelf,
            '晋江文学数据分析': self.j2wx.pull
        })

    @staticmethod
    def add(params_str):
        logging.info('hello, job!')

    def update_bookshelf(self):
        logging.info('start to update bookshelf.')
        self.novel.update_bookshelf()
        pass
