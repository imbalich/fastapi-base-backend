#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：router.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:19 
'''
from fastapi import APIRouter

from backend.app.admin.api.v1.auth import router as auth_router
from backend.app.admin.api.v1.oauth2 import router as oauth2_router
from backend.app.admin.api.v1.sys import router as sys_router
from backend.app.admin.api.v1.log import router as log_router
from backend.app.admin.api.v1.monitor import router as monitor_router

v1 = APIRouter()

v1.include_router(auth_router)
v1.include_router(oauth2_router)
v1.include_router(sys_router)
v1.include_router(log_router)
v1.include_router(monitor_router)
