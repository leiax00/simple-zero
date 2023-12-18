# !/usr/bin/env python
# -*- coding: utf-8 -*-
from contextlib import contextmanager
from typing import Optional

from pydantic import BaseModel
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from szpy.config.data_source import BaseConfig

SQLBase = declarative_base()


class DBConfig(BaseModel):
    url: Optional[str] = None


class DBClient:
    config: DBConfig = None
    __connect_args: dict = {}
    __engine: Engine = None
    __sessionLocal: sessionmaker = None

    def __init__(self, config: DBConfig = None):
        self.init(config)

    def init(self, config: DBConfig = None):
        if config is None:
            return
        try:
            self.config = config
            if self.config.url is not None:
                if 'sqlite' in self.config.url:
                    self.__connect_args['check_same_thread'] = False
            self.engine()
            self.session_local()
            print('db init finished!')
        except Exception as e:
            print(e)

    def engine(self):
        if self.__engine is None:
            self.__engine = create_engine(self.config.url, connect_args=self.__connect_args)
        return self.__engine

    def session_local(self):
        if self.__sessionLocal is None:
            self.__sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.__engine)
        return self.__sessionLocal

    def session(self):
        d = self.__sessionLocal()
        try:
            yield d
        finally:
            d.close()

    @contextmanager
    def context(self):
        d = self.__sessionLocal()
        try:
            yield d
        finally:
            d.close()

    def on_update(self, conf: BaseConfig):
        key = 'db'
        conf.register_changed_event(key, lambda: self.init(conf.db))


client = DBClient()

if __name__ == '__main__':
    pass
