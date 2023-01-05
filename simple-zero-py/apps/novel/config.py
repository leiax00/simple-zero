# !/usr/bin/env python
# -*- coding: utf-8 -*-
from utils.dbHelper import DbHelper
from xxl_executor.executor import XxlExecutor

config = {
    'host': '0.0.0.0',
    'port': 11000,
    'xxl-config': {
        'admin_url': 'http://10.1.0.7:15000/',
        'access_token': 'default_token',
        'executor_name': 'xxl-novel-executor',
        'registry_url': 'http://10.1.0.1:11000/',
        'consume_period': 5,  # xxl-jobx消费线程空转时检测周期
        'consume_async_num': 20,  # xxl-job任务执行并发数量
    }
}

helper = DbHelper(user='postgres', password='lax4832.', host='10.1.0.3', port=5432, database='simple-zero')
db = helper.db_session()

xxl = XxlExecutor(config.get('xxl-config'))