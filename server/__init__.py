# server/__init__.py
from __future__ import absolute_import, unicode_literals

import pymysql
from .celery import app as celery_app

__all__ = ('celery_app',)

pymysql.install_as_MySQLdb()
