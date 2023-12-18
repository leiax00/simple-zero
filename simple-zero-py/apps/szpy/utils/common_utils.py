# !/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os


def set_time_zone(tz='Asia/Chongqing'):
    if 'TZ' not in os.environ:
        # 如果不存在，手动设置所需的时区
        os.environ['TZ'] = tz

        # 使环境变量设置生效
        if hasattr(datetime, '_called_from_timeset_timezone'):
            raise ValueError("Timezone already set.")
        datetime._called_from_timeset_timezone = True
        try:
            datetime.datetime.utcnow()
        finally:
            del datetime._called_from_timeset_timezone


def is_empty_string(string: str) -> bool:
    return string is None or string.strip() == ''
