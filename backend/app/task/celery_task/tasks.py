#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : tasks.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:05
'''
from anyio import sleep

from backend.app.task.celery import celery_app


@celery_app.task(name='task_demo_async')
async def task_demo_async() -> str:
    await sleep(20)
    return 'test async'
