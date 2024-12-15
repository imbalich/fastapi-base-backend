#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : router.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 22:06
'''
from fastapi import APIRouter

from backend.app.task.api.v1.task import router as task_router

v1 = APIRouter()

v1.include_router(task_router, prefix='/tasks', tags=['任务'])