# !/usr/bin/env python
# -*- coding: utf-8 -*-

from data.j2wx.j2wx_parser import J2wxParserFactory, Collector
from utils.httpHelper import *

domain = 'https://app-cdn.jjwxc.com/'


class APIS(Enum):
    # 古言app首页
    gywx_home = Api('/bookstore/getFullPageV1?channel=gywx&version=9', HttpMethod.GET)


class J2wxPuller:
    def __init__(self):
        self.client = HttpSession(domain)
        self.parser = J2wxParserFactory()

    def pull(self, param=None) -> Collector:
        param = APIS.gywx_home.value.get_request_params()
        with self.client.request(**param, verify=False) as resp:
            data_list = resp.json().get('data')
        return self.parser.parse(data_list)


j2wx_puller = J2wxPuller()
