# !/usr/bin/env python
# -*- coding: utf-8 -*-

from apscheduler.schedulers.blocking import BlockingScheduler


class Scheduler(object):
    def __init__(self):
        self.scheduler = BlockingScheduler()

    def start(self):
        self.scheduler.start()

    def add_job(self, func, trigger=None, args=None, kwargs=None, id=None, name=None):
        return self.scheduler.add_job(func, trigger, args, kwargs, id, name)
