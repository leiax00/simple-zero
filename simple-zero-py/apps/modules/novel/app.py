# !/usr/bin/env python
# -*- coding: utf-8 -*-
from szpy.config.app_config import app_conf
from szpy.config.c_nacos import nacos_manager
from szpy.modules import xxl
from szpy.modules.db import sqlalchemy, redis


class AppMgr:
    @staticmethod
    def init():
        print('start to init App!')
        # 注册配置数据源
        app_conf.register_data_source(nacos_manager())

        print(app_conf.model_dump())
        # 初始化xxl
        xxl.client.on_update(app_conf)
        # 初始化数据库
        sqlalchemy.client.on_update(app_conf)
        redis.aio_mgr.on_update(app_conf)

    @staticmethod
    def release():
        print('Start to destroy app!')
        # 移除xxl的执行器
        xxl.client.unregister()
