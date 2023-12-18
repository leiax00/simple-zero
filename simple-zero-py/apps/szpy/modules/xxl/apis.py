# !/usr/bin/env python
# -*- coding: utf-8 -*-
from szpy.entity.bo.api import API

call_back = API(url='/api/callback', method='POST')
register = API(url='/api/registry', method='POST')
unregister = API(url='/api/registryRemove', method='POST')
