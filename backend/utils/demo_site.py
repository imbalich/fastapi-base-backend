#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：demo_site.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:40 
'''
from fastapi import Request

from backend.common.exception import errors
from backend.core.conf import settings


async def demo_site(request: Request):
    """演示站点"""

    method = request.method
    path = request.url.path
    if (
        settings.DEMO_MODE
        and method != 'GET'
        and method != 'OPTIONS'
        and (method, path) not in settings.DEMO_MODE_EXCLUDE
    ):
        raise errors.ForbiddenError(msg='演示环境下禁止执行此操作')