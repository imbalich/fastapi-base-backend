#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Project : PyCharm
@File    : actions.py
@IDE     : Pycharm
@Author  : imbalich
@Time    : 2024/12/15 21:58
'''
from backend.common.socketio.server import sio


async def task_notification(msg: str):
    """
    任务通知

    :param msg:
    :return:
    """
    await sio.emit('task_notification', {'msg': msg})