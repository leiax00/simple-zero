# !/usr/bin/env python
# -*- coding: utf-8 -*-
import argparse
from enum import Enum


class Cmd(Enum):
    BUILD = 0
    DOCKER_IMG = 1
    DOCKER_RUN = 2


class Config:
    name = ''
    version = 'v0.1.0'


if __name__ == '__main__':
    def with_param():
        parser = argparse.ArgumentParser(description='manual to this script')
        parser.add_argument("-name", type=str, default=Config.name)  # 指定app名称
        parser.add_argument("-version", type=str, default=Config.version)  # 指定版本
        parser.add_argument("-cmd", type=str, default=Cmd.BUILD)
        return parser.parse_args()
