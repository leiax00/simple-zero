# !/usr/bin/env python
# -*- coding: utf-8 -*-
import redis

from utils.dbHelper import DbHelper
from xxl_executor.executor import XxlExecutor

config = {
    'host': '0.0.0.0',
    'port': 80,
    'xxl-config': {
        'admin_url': 'http://10.1.0.7:15000/',
        'access_token': 'default_token',
        'executor_name': 'xxl-novel-executor',
        'registry_url': 'http://10.1.0.1:11000/',
        'consume_period': 5,  # xxl-jobx消费线程空转时检测周期
        'consume_async_num': 20,  # xxl-job任务执行并发数量
    }
}

helper = DbHelper(user='leiax00', password='lax4832.', host='10.1.0.3', port=3308, database='simple-zero')
db = helper.db_session()

redis_pool = redis.ConnectionPool(host='10.1.0.3', port=6379, decode_responses=True, db=1)  # apps/sz-novel/...
c_redis = redis.Redis(connection_pool=redis_pool)
REDIS_KEY_PREFIX = 'apps/sz-novel'

xxl = XxlExecutor(config.get('xxl-config'))

if __name__ == '__main__':
    c_redis.set('test', 'hello, redis')
    print(c_redis.get('test'))
