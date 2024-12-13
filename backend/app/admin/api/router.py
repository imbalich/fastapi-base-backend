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

v1 = APIRouter()

v1.include_router(auth_router)
