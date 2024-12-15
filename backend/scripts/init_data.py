#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : init_data.py.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:47
'''
import logging
import sys

from anyio import run

sys.path.append('../')

from backend.database.db_mysql import create_table

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init() -> None:
    logger.info('Creating initial data')
    await create_table()
    logger.info('Initial data created')


if __name__ == '__main__':
    run(init)  # type: ignore
