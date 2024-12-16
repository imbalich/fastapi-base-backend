#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/16 16:09 
'''
from fastapi import APIRouter

from backend.app.admin.api.v1.log.login_log import router as login_log
from backend.app.admin.api.v1.log.opera_log import router as opera_log

router = APIRouter(prefix='/logs')

router.include_router(login_log, prefix='/login', tags=['登录日志'])
router.include_router(opera_log, prefix='/opera', tags=['操作日志'])