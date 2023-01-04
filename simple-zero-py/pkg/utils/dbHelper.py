# !/usr/bin/env python
# -*- coding: utf-8 -*-
import psycopg2
from peewee import PostgresqlDatabase


class DbHelper:
    def __init__(self, user=None, password=None, host=None, port=None, database=None):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        self._db = None

    def with_db(self, user, password, host, port, database):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.database = database
        return self

    def connect(self):
        if self._db is not None:
            self._db.close()
        return self.db_session()

    def db_session(self):
        if self._db is None:
            self._db = PostgresqlDatabase(
                user=self.user,
                password=self.password,
                host=self.host,
                port=self.port,
                database=self.database,
            )
        return self._db
