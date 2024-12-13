#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''
@Project ：fastapi-base-backend 
@File    ：__init__.py.py
@IDE     ：PyCharm 
@Author  ：imbalich
@Date    ：2024/12/13 16:20 
'''
from fastapi import APIRouter

from backend.app.admin.api.v1.auth.auth import router as auth_router
from backend.app.admin.api.v1.auth.captcha import router as captcha_router

router = APIRouter(prefix='/auth')

router.include_router(auth_router, tags=['授权'])
router.include_router(captcha_router, prefix='/captcha', tags=['验证码'])