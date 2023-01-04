# !/usr/bin/env python
# -*- coding: utf-8 -*-
import abc


class IJob:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def revert_join(self, executor):
        raise NotImplemented('请实现该接口')
