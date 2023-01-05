# !/usr/bin/env python
# -*- coding: utf-8 -*-
from extender.serial_extender import Serialize


class XxlConfig:
    def __init__(self):
        self.admin_url = None
        self.access_token = None
        self.executor_name = None
        self.registry_url = None
        self.consume_period = 5
        self.consume_async_num = 20

    def fill(self, params: dict = {}):
        self.__dict__ = {**self.__dict__, **params}
        return self


class XxlTask(Serialize):
    def __init__(self):
        self.job_id = None
        self.job_name = None
        self.job_params = None
        self.block_strategy = None
        self.timeout = None
        self.log_id = None
        self.log_time = None
        self.glue_type = None
        self.glue_src = None
        self.glue_update_time = None
        self.broadcast_index = None
        self.broadcast_total = None

    def fill(self, params: dict = {}):
        self.__dict__ = {**self.__dict__, **params}
        return self

    def fill_with_req(self, req_json):
        self.job_id = req_json.get('jobId')
        self.job_name = req_json.get('executorHandler')
        self.job_params = req_json.get('executorParams')
        self.block_strategy = req_json.get('executorBlockStrategy')
        self.timeout = req_json.get('executorTimeout')
        self.log_id = req_json.get('logId')
        self.log_time = req_json.get('logDateTime')
        self.glue_type = req_json.get('glueType')
        self.glue_src = req_json.get('glueSource')
        self.glue_update_time = req_json.get('glueUpdatetime')
        self.broadcast_index = req_json.get('broadcastIndex')
        self.broadcast_total = req_json.get('broadcastTotal')
        return self